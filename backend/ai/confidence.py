"""Transparent heuristic confidence scoring for extracted cadastral candidates."""
from typing import Dict, Any
import math

class ConfidenceEngine:
    """Calculates explainable confidence scores for candidate features."""

    @staticmethod
    def calculate_parcel_confidence(area_m2: float, perimeter_m: float, vertex_count: int) -> float:
        """Calculates heuristic confidence based on geometric compactness and cadastral parcel norms.
        Parcels with clean rectangular/polygonal shapes score higher.
        """
        if perimeter_m <= 0 or area_m2 <= 0:
            return 0.50

        # Isoperimetric quotient (compactness): 4 * pi * Area / Perimeter^2
        # Circle = 1.0, Square = ~0.785, long thin strip = < 0.2
        compactness = (4.0 * math.pi * area_m2) / (perimeter_m ** 2)

        # Urban parcel heuristics
        score = 0.85
        if 0.4 <= compactness <= 0.85:
            score += 0.08  # Typical healthy urban lot
        elif compactness < 0.25:
            score -= 0.15  # Potentially irregular or sliver

        if 4 <= vertex_count <= 8:
            score += 0.04  # Clean cadastral boundary
        elif vertex_count > 20:
            score -= 0.06  # Noisy boundary requiring simplification

        return round(max(0.40, min(0.98, score)), 2)

    @staticmethod
    def calculate_building_confidence(area_m2: float, aspect_ratio: float = 1.2) -> float:
        """Calculates heuristic confidence for building footprints."""
        if area_m2 < 15.0:  # Micro-structure or shed
            return 0.72
        elif 50.0 <= area_m2 <= 800.0:  # Typical residential/commercial roof
            return 0.94
        return 0.88
