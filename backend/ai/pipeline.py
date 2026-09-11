"""Unified AI/CV Extraction Pipeline Orchestrator."""
from typing import List, Dict, Any, Tuple
import os
from backend.models.domain import ProcessingMode
from backend.ai.fixture_extractor import FixtureExtractor
from backend.ai.cv_extractor import CVExtractor

class ExtractionPipeline:
    """Orchestrates candidate extraction across model_inference, cv_baseline, and demo_fixture."""

    def __init__(self, fixtures_dir: str = "fixtures/geojson", imagery_dir: str = "fixtures/imagery"):
        self.fixture_extractor = FixtureExtractor(fixtures_dir)
        self.imagery_dir = imagery_dir

    def run_extraction(
        self,
        project_id: str,
        asset_id: str,
        feature_types: List[str],
        requested_mode: ProcessingMode = "cv_baseline"
    ) -> Tuple[List[Dict[str, Any]], ProcessingMode, Dict[str, Any]]:
        """Executes extraction and returns (features, actual_mode_used, summary_dict)."""
        actual_mode: ProcessingMode = requested_mode

        # 1. Demo Fixture Mode
        if requested_mode == "demo_fixture":
            features = self.fixture_extractor.extract_features(project_id, asset_id, feature_types)
            return features, "demo_fixture", self._summarize(features)

        # 2. CV Baseline Mode
        image_path = os.path.join(self.imagery_dir, "sample_ortho.jpg")
        bounds = {"west": 77.5910, "south": 12.9685, "east": 77.5982, "north": 12.9747}

        if requested_mode == "cv_baseline":
            try:
                cv_engine = CVExtractor(image_path, bounds)
                features = cv_engine.extract(project_id, asset_id, feature_types)
                if not features:
                    # Graceful fallback to verified fixtures
                    features = self.fixture_extractor.extract_features(project_id, asset_id, feature_types)
                    actual_mode = "demo_fixture"
            except Exception:
                features = self.fixture_extractor.extract_features(project_id, asset_id, feature_types)
                actual_mode = "demo_fixture"

            return features, actual_mode, self._summarize(features)

        # 3. Model Inference (Pretrained adapter with instant fallback)
        if requested_mode == "model_inference":
            # Live model checkpoint or GPU not present in baseline environment -> fallback to CV baseline
            try:
                cv_engine = CVExtractor(image_path, bounds)
                features = cv_engine.extract(project_id, asset_id, feature_types)
                actual_mode = "cv_baseline"
            except Exception:
                features = self.fixture_extractor.extract_features(project_id, asset_id, feature_types)
                actual_mode = "demo_fixture"

            return features, actual_mode, self._summarize(features)

        # Default fallback
        features = self.fixture_extractor.extract_features(project_id, asset_id, feature_types)
        return features, "demo_fixture", self._summarize(features)

    def _summarize(self, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        parcels = sum(1 for f in features if f.get("featureType") == "parcel")
        buildings = sum(1 for f in features if f.get("featureType") == "building")
        roads = sum(1 for f in features if f.get("featureType") == "road")
        confidences = [f.get("properties", {}).get("confidence", 0.9) for f in features if f.get("properties", {}).get("confidence")]
        mean_conf = round(sum(confidences) / len(confidences), 2) if confidences else 0.90

        return {
            "parcels": parcels,
            "buildings": buildings,
            "roads": roads,
            "total": len(features),
            "meanConfidence": mean_conf
        }
