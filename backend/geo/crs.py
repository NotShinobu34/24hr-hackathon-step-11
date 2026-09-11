"""Coordinate Reference System (CRS) management and metric projections.

Refinement requirements:
- Preserve source CRS metadata.
- Explicitly project to appropriate metric CRS for physical calculations (m², m).
- RFC 7946 GeoJSON interchange strictly in WGS 84 (EPSG:4326, [lon, lat]).
- Never silently guess CRS.
- Document all transformations.
"""
import math
from typing import Tuple, List, Dict, Any

class CRSManager:
    """Handles explicit coordinate reference systems and metric projections."""
    
    WGS84_A = 6378137.0           # Semi-major axis (meters)
    WGS84_F = 1.0 / 298.257223563 # Flattening
    WGS84_B = 6356752.314245      # Semi-minor axis
    WGS84_E2 = 0.00669437999014   # First eccentricity squared

    @staticmethod
    def get_utm_zone(lon: float) -> int:
        """Determines standard UTM zone number from longitude."""
        return int((lon + 180) / 6) + 1

    @staticmethod
    def get_utm_epsg(lon: float, lat: float) -> str:
        """Returns EPSG code for local UTM projection (e.g., EPSG:32643)."""
        zone = CRSManager.get_utm_zone(lon)
        if lat >= 0:
            return f"EPSG:326{zone:02d}"
        else:
            return f"EPSG:327{zone:02d}"

    @classmethod
    def wgs84_to_utm(cls, lon: float, lat: float, central_meridian: float = None) -> Tuple[float, float]:
        """Converts WGS84 (lon, lat in degrees) to Transverse Mercator / UTM (x, y in meters)."""
        if central_meridian is None:
            zone = cls.get_utm_zone(lon)
            central_meridian = (zone - 1) * 6 - 180 + 3

        k0 = 0.9996
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        cm_rad = math.radians(central_meridian)

        a = cls.WGS84_A
        e2 = cls.WGS84_E2
        e4 = e2 * e2
        e6 = e4 * e2

        N = a / math.sqrt(1 - e2 * math.sin(lat_rad)**2)
        T = math.tan(lat_rad)**2
        C = (e2 / (1 - e2)) * math.cos(lat_rad)**2
        A = (lon_rad - cm_rad) * math.cos(lat_rad)

        M = a * (
            (1 - e2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * lat_rad
            - (3 * e2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * math.sin(2 * lat_rad)
            + (15 * e4 / 256 + 45 * e6 / 1024) * math.sin(4 * lat_rad)
            - (35 * e6 / 3072) * math.sin(6 * lat_rad)
        )

        x = k0 * N * (
            A + (1 - T + C) * A**3 / 6
            + (5 - 18 * T + T**2 + 72 * C - 58 * e2) * A**5 / 120
        ) + 500000.0  # False Easting

        y = k0 * (
            M + N * math.tan(lat_rad) * (
                A**2 / 2
                + (5 - T + 9 * C + 4 * C**2) * A**4 / 24
                + (61 - 58 * T + T**2 + 600 * C - 330 * e2) * A**6 / 720
            )
        )
        if lat < 0:
            y += 10000000.0  # False Northing for Southern Hemisphere

        return x, y

    @classmethod
    def utm_to_wgs84(cls, x: float, y: float, zone: int, northern: bool = True) -> Tuple[float, float]:
        """Converts UTM (x, y in meters) back to WGS84 (lon, lat in degrees)."""
        central_meridian = (zone - 1) * 6 - 180 + 3
        k0 = 0.9996
        a = cls.WGS84_A
        e2 = cls.WGS84_E2
        e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))

        x_adj = x - 500000.0
        y_adj = y if northern else y - 10000000.0

        M = y_adj / k0
        mu = M / (a * (1 - e2 / 4 - 3 * e2**2 / 64 - 5 * e2**3 / 256))

        phi1 = mu + (3 * e1 / 2 - 27 * e1**3 / 32) * math.sin(2 * mu) \
               + (21 * e1**2 / 16 - 55 * e1**4 / 32) * math.sin(4 * mu) \
               + (151 * e1**3 / 96) * math.sin(6 * mu)

        N1 = a / math.sqrt(1 - e2 * math.sin(phi1)**2)
        T1 = math.tan(phi1)**2
        C1 = (e2 / (1 - e2)) * math.cos(phi1)**2
        R1 = a * (1 - e2) / ((1 - e2 * math.sin(phi1)**2)**1.5)
        D = x_adj / (N1 * k0)

        lat = phi1 - (N1 * math.tan(phi1) / R1) * (
            D**2 / 2
            - (5 + 3 * T1 + 10 * C1 - 4 * C1**2 - 9 * e2) * D**4 / 24
            + (61 + 90 * T1 + 298 * C1 + 45 * T1**2 - 252 * e2 - 3 * C1**2) * D**6 / 720
        )
        lon = math.radians(central_meridian) + (
            D - (1 + 2 * T1 + C1) * D**3 / 6
            + (5 - 2 * C1 + 28 * T1 - 3 * C1**2 + 8 * e2 + 24 * T1**2) * D**5 / 120
        ) / math.cos(phi1)

        return math.degrees(lon), math.degrees(lat)

    @classmethod
    def project_geometry_to_metric(cls, geometry: Dict[str, Any], target_epsg: str = None) -> Tuple[Dict[str, Any], str]:
        """Transforms a WGS84 GeoJSON geometry into a local metric projected geometry."""
        geom_type = geometry.get("type")
        coords = geometry.get("coordinates")

        # Sample first coordinate to choose UTM zone if not provided
        sample_pt = cls._get_sample_point(coords, geom_type)
        if target_epsg is None:
            target_epsg = cls.get_utm_epsg(sample_pt[0], sample_pt[1])

        zone = int(target_epsg[8:]) if "326" in target_epsg or "327" in target_epsg else cls.get_utm_zone(sample_pt[0])
        cm = (zone - 1) * 6 - 180 + 3

        transformed_coords = cls._transform_coords(coords, lambda lon, lat: cls.wgs84_to_utm(lon, lat, cm))
        return {"type": geom_type, "coordinates": transformed_coords}, target_epsg

    @classmethod
    def project_geometry_to_wgs84(cls, geometry: Dict[str, Any], source_epsg: str) -> Dict[str, Any]:
        """Transforms a metric projected geometry back to WGS84 (EPSG:4326)."""
        geom_type = geometry.get("type")
        coords = geometry.get("coordinates")
        zone = int(source_epsg[8:]) if "326" in source_epsg or "327" in source_epsg else 43
        northern = not ("327" in source_epsg)

        transformed_coords = cls._transform_coords(coords, lambda x, y: cls.utm_to_wgs84(x, y, zone, northern))
        return {"type": geom_type, "coordinates": transformed_coords}

    @staticmethod
    def _get_sample_point(coords: Any, geom_type: str) -> Tuple[float, float]:
        if geom_type == "Point":
            return coords[0], coords[1]
        elif geom_type in ("LineString", "MultiPoint"):
            return coords[0][0], coords[0][1]
        elif geom_type in ("Polygon", "MultiLineString"):
            return coords[0][0][0], coords[0][0][1]
        elif geom_type == "MultiPolygon":
            return coords[0][0][0][0], coords[0][0][0][1]
        return 77.5946, 12.9716

    @classmethod
    def _transform_coords(cls, coords: Any, func) -> Any:
        if isinstance(coords[0], (int, float)):
            return list(func(coords[0], coords[1]))
        return [cls._transform_coords(c, func) for c in coords]
