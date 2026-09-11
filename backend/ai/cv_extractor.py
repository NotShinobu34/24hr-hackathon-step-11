"""OpenCV baseline computer vision extraction pipeline."""
import os
import cv2
import numpy as np
from typing import List, Dict, Any
import uuid
from backend.ai.confidence import ConfidenceEngine
from backend.geo.geometry import GeometryEngine

class CVExtractor:
    """Extracts candidate parcel and building polygon features using OpenCV."""

    def __init__(self, image_path: str, bounds: Dict[str, float]):
        self.image_path = image_path
        self.bounds = bounds # {west, south, east, north}

    def pixel_to_geo(self, px: float, py: float, width: int, height: int) -> List[float]:
        """Maps pixel coordinate [px, py] to WGS84 geographic coordinate [lon, lat]."""
        lon = self.bounds["west"] + (px / width) * (self.bounds["east"] - self.bounds["west"])
        lat = self.bounds["north"] - (py / height) * (self.bounds["north"] - self.bounds["south"])
        return [round(lon, 6), round(lat, 6)]

    def extract(self, project_id: str, asset_id: str, feature_types: List[str]) -> List[Dict[str, Any]]:
        features: List[Dict[str, Any]] = []

        if not os.path.exists(self.image_path):
            return features

        img = cv2.imread(self.image_path)
        if img is None:
            return features

        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Baseline morphological filter to isolate building roofs and parcel boundaries
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(edges, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area_px = cv2.contourArea(cnt)
            if area_px < 400:  # Skip tiny noise
                continue

            # Approximate polygon with Douglas-Peucker epsilon
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) < 4:
                continue

            geo_coords = []
            for pt in approx:
                x, y = pt[0]
                geo_coords.append(self.pixel_to_geo(x, y, width, height))

            # Close polygon ring
            if geo_coords[0] != geo_coords[-1]:
                geo_coords.append(geo_coords[0])

            geom = {"type": "Polygon", "coordinates": [geo_coords]}
            try:
                area_m2, perim_m, _ = GeometryEngine.calculate_metric_measurements(geom)
            except Exception:
                area_m2, perim_m = 250.0, 65.0

            # Distinguish building vs parcel candidate by area
            f_type = "building" if area_m2 < 350.0 else "parcel"
            if f_type not in feature_types:
                continue

            conf = ConfidenceEngine.calculate_parcel_confidence(area_m2, perim_m, len(approx))

            feat_id = f"{f_type[:4]}_{uuid.uuid4().hex[:6]}"
            features.append({
                "type": "Feature",
                "id": feat_id,
                "featureType": f_type,
                "geometry": geom,
                "properties": {
                    "source": "ai",
                    "sourceAssetId": asset_id,
                    "processingMode": "cv_baseline",
                    "confidence": conf,
                    "confidenceType": "heuristic",
                    "status": "detected",
                    "edited": False,
                    "verified": False,
                    "area_m2": area_m2,
                    "perimeter_m": perim_m,
                    "metricCrs": "EPSG:32643"
                }
            })

        return features
