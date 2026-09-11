"""Shapely geometry conversion, validation, and metric measurements."""
from typing import Dict, Any, Tuple, Optional
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.validation import make_valid
from backend.geo.crs import CRSManager

class GeometryEngine:
    """Provides deterministic geometric calculations and Shapely conversions."""

    @staticmethod
    def to_shapely(geojson_geom: Dict[str, Any]):
        """Converts a GeoJSON geometry dictionary to a Shapely geometry object."""
        return shape(geojson_geom)

    @staticmethod
    def to_geojson(shapely_geom) -> Dict[str, Any]:
        """Converts a Shapely geometry object to a standard GeoJSON geometry dict."""
        return mapping(shapely_geom)

    @classmethod
    def calculate_metric_measurements(cls, geojson_geom: Dict[str, Any], metric_epsg: str = None) -> Tuple[float, float, str]:
        """Projects geometry to local metric CRS (e.g. UTM) and computes area (m²) and perimeter (m).
        Returns: (area_m2, perimeter_m, metric_epsg_used)
        """
        projected_geom, epsg_used = CRSManager.project_geometry_to_metric(geojson_geom, target_epsg=metric_epsg)
        s_geom = cls.to_shapely(projected_geom)
        
        area_m2 = round(float(s_geom.area), 2)
        perimeter_m = round(float(s_geom.length), 2)
        return area_m2, perimeter_m, epsg_used

    @classmethod
    def validate_and_repair(cls, geojson_geom: Dict[str, Any]) -> Tuple[Dict[str, Any], bool, Optional[str]]:
        """Validates polygon geometry. Returns (repaired_or_original_geom, is_valid, error_reason)."""
        s_geom = cls.to_shapely(geojson_geom)
        if s_geom.is_valid:
            return geojson_geom, True, None

        # Attempt deterministic repair using Shapely's make_valid
        repaired = make_valid(s_geom)
        return cls.to_geojson(repaired), False, "Geometry contained self-intersections or invalid rings"

    @classmethod
    def simplify_geometry(cls, geojson_geom: Dict[str, Any], tolerance_meters: float = 0.1) -> Dict[str, Any]:
        """Simplifies geometry within a specified tolerance in meters."""
        projected_geom, epsg_used = CRSManager.project_geometry_to_metric(geojson_geom)
        s_geom = cls.to_shapely(projected_geom)
        simplified = s_geom.simplify(tolerance_meters, preserve_topology=True)
        wgs84_simplified = CRSManager.project_geometry_to_wgs84(cls.to_geojson(simplified), epsg_used)
        return wgs84_simplified
