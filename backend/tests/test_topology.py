"""Unit tests for deterministic topology validation engine."""
import unittest
from backend.geo.topology import TopologyValidator

class TestTopologyValidator(unittest.TestCase):

    def setUp(self):
        self.validator = TopologyValidator(overlap_tolerance_m2=0.05, sliver_threshold_m2=2.0)

    def test_valid_polygon(self):
        features = [{
            "id": "p1",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5930, 12.9710], [77.5936, 12.9710], [77.5936, 12.9716], [77.5930, 12.9716], [77.5930, 12.9710]]]
            }
        }]
        issues = self.validator.validate_feature_collection("test_proj", features)
        self.assertEqual(len(issues), 0, "Clean polygon should have no topology issues.")

    def test_self_intersection_bowtie(self):
        # Bowtie polygon (self-intersecting outer ring)
        features = [{
            "id": "p_bowtie",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5930, 12.9710], [77.5940, 12.9720], [77.5940, 12.9710], [77.5930, 12.9720], [77.5930, 12.9710]]]
            }
        }]
        issues = self.validator.validate_feature_collection("test_proj", features)
        self.assertGreaterEqual(len(issues), 1)
        self.assertIn(issues[0].issueType, ("self_intersection", "invalid_geometry"))
        self.assertEqual(issues[0].severity, "high")

    def test_parcel_overlap(self):
        # Two parcels with intentional intersection
        features = [
            {
                "id": "p104",
                "featureType": "parcel",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[77.5949, 12.9710], [77.5956, 12.9710], [77.5956, 12.9716], [77.5949, 12.9716], [77.5949, 12.9710]]]
                }
            },
            {
                "id": "p105",
                "featureType": "parcel",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[77.5954, 12.9710], [77.5962, 12.9710], [77.5962, 12.9716], [77.5954, 12.9716], [77.5954, 12.9710]]]
                }
            }
        ]
        issues = self.validator.validate_feature_collection("test_proj", features)
        overlap_issues = [i for i in issues if i.issueType == "overlap"]
        self.assertEqual(len(overlap_issues), 1, "Should detect exactly 1 overlap between p104 and p105.")
        self.assertEqual(overlap_issues[0].severity, "high")

    def test_shared_edge_no_overlap(self):
        # Two adjacent parcels sharing an exact line border at 77.5936
        features = [
            {
                "id": "lotA",
                "featureType": "parcel",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[77.5930, 12.9710], [77.5936, 12.9710], [77.5936, 12.9716], [77.5930, 12.9716], [77.5930, 12.9710]]]
                }
            },
            {
                "id": "lotB",
                "featureType": "parcel",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[77.5936, 12.9710], [77.5942, 12.9710], [77.5942, 12.9716], [77.5936, 12.9716], [77.5936, 12.9710]]]
                }
            }
        ]
        issues = self.validator.validate_feature_collection("test_proj", features)
        overlap_issues = [i for i in issues if i.issueType == "overlap"]
        self.assertEqual(len(overlap_issues), 0, "Legitimate shared borders should NOT be flagged as overlaps.")

    def test_sliver_detection(self):
        # Tiny micro-polygon (< 2.0 m², approx 0.5m x 0.5m = 0.25 m²)
        features = [{
            "id": "sliver_01",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.593680, 12.971780], [77.593685, 12.971780], [77.593685, 12.971785], [77.593680, 12.971785], [77.593680, 12.971780]]]
            }
        }]
        issues = self.validator.validate_feature_collection("test_proj", features)
        sliver_issues = [i for i in issues if i.issueType == "sliver"]
        self.assertEqual(len(sliver_issues), 1, "Should flag micro-polygon as sliver.")

    def test_duplicate_geometry(self):
        # Two distinct feature IDs with identical coordinates
        coords = [[[77.5930, 12.9710], [77.5936, 12.9710], [77.5936, 12.9716], [77.5930, 12.9716], [77.5930, 12.9710]]]
        features = [
            {"id": "dupA", "featureType": "parcel", "geometry": {"type": "Polygon", "coordinates": coords}},
            {"id": "dupB", "featureType": "parcel", "geometry": {"type": "Polygon", "coordinates": coords}}
        ]
        issues = self.validator.validate_feature_collection("test_proj", features)
        dup_issues = [i for i in issues if i.issueType == "duplicate"]
        self.assertEqual(len(dup_issues), 1, "Should detect duplicate geometry.")

if __name__ == "__main__":
    unittest.main()
