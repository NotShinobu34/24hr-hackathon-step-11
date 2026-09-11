"""Export service for generating RFC 7946 GeoJSON packages."""
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple
import uuid

class ExportService:
    """Produces standardized GIS-ready GeoJSON export packages."""

    def __init__(self, export_dir: str = "data/exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def export_geojson(self, project_id: str, project_name: str, features: List[Dict[str, Any]], include_types: List[str]) -> Tuple[str, str, int]:
        """Filters, packages, and saves GeoJSON. Returns (filename, download_url, feature_count)."""
        filtered = [
            f for f in features 
            if (f.get("featureType") in include_types or f.get("properties", {}).get("featureType") in include_types)
        ]

        geojson_payload = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "metadata": {
                "projectId": project_id,
                "projectName": project_name,
                "exportedAt": datetime.utcnow().isoformat() + "Z",
                "specification": "RFC 7946",
                "geographicCrs": "EPSG:4326",
                "producer": "GeoParcel AI Cadastral Engine",
                "includedFeatureTypes": include_types,
                "totalFeatures": len(filtered)
            },
            "features": filtered
        }

        filename = f"{project_id}_export_{uuid.uuid4().hex[:6]}.geojson"
        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(geojson_payload, f, indent=2)

        download_url = f"/api/exports/download/{filename}"
        return filename, download_url, len(filtered)
