"""Deterministic topology validation engine matching TOPOLOGY_RULES.md.

Refinement requirements:
- Tolerances are configurable project parameters labeled as prototype parameters.
- Shared edges between adjacent parcels MUST NOT trigger false positive overlaps.
- Checks:
  1. Invalid geometry
  2. Self-intersection (bowties)
  3. Parcel overlap (area(A ∩ B) > overlapToleranceM2 in projected metric CRS)
  4. Duplicate geometries
  5. Suspicious slivers (area < sliverThresholdM2)
"""
from typing import List, Dict, Any, Tuple
import uuid
from datetime import datetime, timezone
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.validation import explain_validity
from backend.models.domain import TopologyIssue, IssueSeverity, IssueType
from backend.geo.crs import CRSManager
from backend.geo.geometry import GeometryEngine

class TopologyValidator:
    """Executes deterministic topology checks on cadastral vector features."""

    def __init__(self, overlap_tolerance_m2: float = 0.05, sliver_threshold_m2: float = 2.0):
        self.overlap_tolerance_m2 = overlap_tolerance_m2
        self.sliver_threshold_m2 = sliver_threshold_m2

    def validate_feature_collection(self, project_id: str, features: List[Dict[str, Any]]) -> List[TopologyIssue]:
        """Runs the complete suite of topology checks across all features in a project."""
        issues: List[TopologyIssue] = []

        # 1. Individual geometry validity & sliver checks
        for feat in features:
            f_id = feat.get("id", "unknown")
            geom = feat.get("geometry")
            if not geom or geom.get("type") not in ("Polygon", "MultiPolygon"):
                continue

            # Project to metric CRS for accurate area and shape tests
            proj_geom, epsg = CRSManager.project_geometry_to_metric(geom)
            s_geom = shape(proj_geom)

            # Check 1: Invalid geometry
            if not s_geom.is_valid:
                reason = explain_validity(s_geom)
                issue_type: IssueType = "self_intersection" if "Self-intersection" in reason else "invalid_geometry"
                severity: IssueSeverity = "high"
                issues.append(TopologyIssue(
                    id=f"issue_{uuid.uuid4().hex[:8]}",
                    projectId=project_id,
                    featureId=f_id,
                    relatedFeatureId=None,
                    issueType=issue_type,
                    severity=severity,
                    message=f"Feature {f_id} has invalid geometry: {reason}",
                    toleranceUsed=0.0,
                    resolved=False,
                    createdAt=datetime.utcnow().isoformat() + "Z"
                ))
                continue  # Skip further checks on invalid geometries until repaired

            # Check 5: Suspicious slivers (only for parcels)
            if feat.get("featureType") == "parcel" or feat.get("properties", {}).get("featureType") == "parcel":
                area_m2 = float(s_geom.area)
                if area_m2 < self.sliver_threshold_m2:
                    issues.append(TopologyIssue(
                        id=f"issue_{uuid.uuid4().hex[:8]}",
                        projectId=project_id,
                        featureId=f_id,
                        relatedFeatureId=None,
                        issueType="sliver",
                        severity="medium",
                        message=f"Parcel {f_id} has area {area_m2:.2f} m², which is below the prototype sliver threshold of {self.sliver_threshold_m2} m².",
                        toleranceUsed=self.sliver_threshold_m2,
                        resolved=False,
                        createdAt=datetime.utcnow().isoformat() + "Z"
                    ))

        # 2. Pairwise checks (overlaps and duplicates among parcels)
        parcel_features = [
            f for f in features 
            if f.get("featureType") == "parcel" or f.get("properties", {}).get("featureType") == "parcel"
        ]

        # Prepare projected shapely geometries for fast intersection testing
        projected_parcels = []
        for feat in parcel_features:
            geom = feat.get("geometry")
            if geom and geom.get("type") in ("Polygon", "MultiPolygon"):
                proj_geom, epsg = CRSManager.project_geometry_to_metric(geom)
                s_geom = shape(proj_geom)
                if s_geom.is_valid:
                    projected_parcels.append((feat.get("id"), s_geom))

        n = len(projected_parcels)
        for i in range(n):
            id_a, geom_a = projected_parcels[i]
            for j in range(i + 1, n):
                id_b, geom_b = projected_parcels[j]

                # Fast bounding-box rejection test
                if not geom_a.bounds or not geom_b.bounds:
                    continue
                minx_a, miny_a, maxx_a, maxy_a = geom_a.bounds
                minx_b, miny_b, maxx_b, maxy_b = geom_b.bounds
                if (maxx_a < minx_b or maxx_b < minx_a or maxy_a < miny_b or maxy_b < miny_a):
                    continue

                # Check 4: Duplicate geometry check (near-identical or identical)
                if geom_a.equals_exact(geom_b, tolerance=0.01):
                    issues.append(TopologyIssue(
                        id=f"issue_{uuid.uuid4().hex[:8]}",
                        projectId=project_id,
                        featureId=id_a,
                        relatedFeatureId=id_b,
                        issueType="duplicate",
                        severity="high",
                        message=f"Duplicate geometry detected between parcel {id_a} and parcel {id_b}.",
                        toleranceUsed=0.01,
                        resolved=False,
                        createdAt=datetime.utcnow().isoformat() + "Z"
                    ))
                    continue

                # Check 3: Parcel overlap check
                if geom_a.intersects(geom_b):
                    try:
                        inter = geom_a.intersection(geom_b)
                        inter_area = float(inter.area) if hasattr(inter, "area") else 0.0

                        # Legitimate shared borders have area 0.0 (dimension 1). Flag only if area > tolerance!
                        if inter_area > self.overlap_tolerance_m2:
                            issues.append(TopologyIssue(
                                id=f"issue_{uuid.uuid4().hex[:8]}",
                                projectId=project_id,
                                featureId=id_a,
                                relatedFeatureId=id_b,
                                issueType="overlap",
                                severity="high",
                                message=f"Overlapping parcel boundaries detected between {id_a} and {id_b}. Overlap area: {inter_area:.2f} m² (tolerance: {self.overlap_tolerance_m2} m²).",
                                toleranceUsed=self.overlap_tolerance_m2,
                                resolved=False,
                                createdAt=datetime.utcnow().isoformat() + "Z"
                            ))
                    except Exception:
                        pass

        return issues
