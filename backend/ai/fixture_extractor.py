"""High-reliability fixture extractor providing guaranteed fallback capability."""
import json
import os
from typing import List, Dict, Any

class FixtureExtractor:
    """Loads curated demo fixtures with full provenance metadata."""

    def __init__(self, fixtures_dir: str = "fixtures/geojson"):
        self.fixtures_dir = fixtures_dir

    def extract_features(self, project_id: str, asset_id: str, feature_types: List[str]) -> List[Dict[str, Any]]:
        extracted: List[Dict[str, Any]] = []

        type_to_file = {
            "parcel": "parcels_detected.geojson",
            "building": "buildings_detected.geojson",
            "road": "roads_detected.geojson"
        }

        for f_type in feature_types:
            filename = type_to_file.get(f_type)
            if not filename:
                continue

            filepath = os.path.join(self.fixtures_dir, filename)
            if not os.path.exists(filepath):
                # Fallback relative check
                alt_path = os.path.join("..", self.fixtures_dir, filename)
                if os.path.exists(alt_path):
                    filepath = alt_path
                else:
                    continue

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            for feat in data.get("features", []):
                # Ensure provenance tags match active request
                feat["properties"]["sourceAssetId"] = asset_id
                feat["properties"]["processingMode"] = "demo_fixture"
                feat["projectId"] = project_id
                extracted.append(feat)

        return extracted
