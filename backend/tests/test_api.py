"""Integration tests for FastAPI endpoints."""
import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestAPIIntegration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["services"]["gis_engine"], "available")

    def test_get_project(self):
        res = self.client.get("/api/projects/project-001")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["project"]["id"], "project-001")
        self.assertEqual(data["project"]["name"], "Ward 12 Survey")

    def test_get_features(self):
        res = self.client.get("/api/projects/project-001/features")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["type"], "FeatureCollection")
        self.assertGreater(len(data["features"]), 0)

    def test_validate_topology_detects_overlap(self):
        res = self.client.post("/api/projects/project-001/validate")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("valid", data)
        self.assertIn("issues", data)
        overlap_issues = [i for i in data["issues"] if i["issueType"] == "overlap"]
        self.assertGreaterEqual(len(overlap_issues), 1, "Should detect the intentional P-104/P-105 overlap in demo fixtures.")

    def test_patch_feature_and_revalidate(self):
        # 1. Inspect P-104 before edit
        res = self.client.get("/api/projects/project-001/features/parcel-104")
        self.assertEqual(res.status_code, 200)

        # 2. Fix the overlap by pulling P-104 east edge back to 77.5954 (clearing overlap with P-105 at 77.59545)
        clean_geom = {
            "type": "Polygon",
            "coordinates": [[[77.5949, 12.9710], [77.5954, 12.9710], [77.5954, 12.9716], [77.5949, 12.9716], [77.5949, 12.9710]]]
        }
        patch_res = self.client.patch("/api/projects/project-001/features/parcel-104", json={"geometry": clean_geom})
        self.assertEqual(patch_res.status_code, 200)
        patched_feat = patch_res.json()
        self.assertEqual(patched_feat["properties"]["status"], "corrected")
        self.assertTrue(patched_feat["properties"]["edited"])

        # 3. Revalidate -> overlap between P-104 and P-105 should be resolved!
        val_res = self.client.post("/api/projects/project-001/validate")
        self.assertEqual(val_res.status_code, 200)
        val_data = val_res.json()
        p104_overlaps = [i for i in val_data["issues"] if i["featureId"] == "parcel-104" and i["issueType"] == "overlap"]
        self.assertEqual(len(p104_overlaps), 0, "P-104 overlap should be cleared after geometry correction.")

    def test_export_geojson(self):
        res = self.client.post("/api/projects/project-001/export", json={"format": "geojson", "include": ["parcel", "building", "road"]})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "completed")
        self.assertIn("downloadUrl", data)
        self.assertGreater(data["featureCount"], 0)

if __name__ == "__main__":
    unittest.main()
