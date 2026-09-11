"""Unit tests for metric projection and geometry calculations."""
import unittest
from backend.geo.crs import CRSManager
from backend.geo.geometry import GeometryEngine

class TestGeometryEngine(unittest.TestCase):

    def test_utm_projection_and_area(self):
        # 0.0006 deg lon x 0.0006 deg lat around Bangalore (12.97 N, 77.59 E)
        # 0.0006 deg lon ~ 65.2 m; 0.0006 deg lat ~ 66.3 m -> expected area ~ 4300 - 4400 m²
        geom = {
            "type": "Polygon",
            "coordinates": [[[77.5930, 12.9710], [77.5936, 12.9710], [77.5936, 12.9716], [77.5930, 12.9716], [77.5930, 12.9710]]]
        }
        area_m2, perimeter_m, epsg = GeometryEngine.calculate_metric_measurements(geom)
        
        self.assertEqual(epsg, "EPSG:32643", "Should detect UTM Zone 43N for longitude 77.59")
        self.assertGreater(area_m2, 4000.0)
        self.assertLess(area_m2, 4800.0)
        self.assertGreater(perimeter_m, 200.0)
        self.assertLess(perimeter_m, 300.0)

    def test_utm_roundtrip(self):
        lon, lat = 77.5946, 12.9716
        x, y = CRSManager.wgs84_to_utm(lon, lat)
        lon_back, lat_back = CRSManager.utm_to_wgs84(x, y, zone=43, northern=True)
        self.assertAlmostEqual(lon, lon_back, places=5)
        self.assertAlmostEqual(lat, lat_back, places=5)

if __name__ == "__main__":
    unittest.main()
