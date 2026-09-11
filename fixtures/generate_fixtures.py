import json
import os

os.makedirs('fixtures/geojson', exist_ok=True)

# 1. PARCELS DETECTED (includes 1 intentional overlap between parcel-104 and parcel-105, plus 1 sliver parcel-112)
parcels = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [
        {
            "type": "Feature",
            "id": "parcel-101",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5930, 12.9710], [77.5936, 12.9710], [77.5936, 12.9716], [77.5930, 12.9716], [77.5930, 12.9710]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.94,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 441.2,
                "perimeter_m": 84.0,
                "land_use": "residential",
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "parcel-102",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5936, 12.9710], [77.5942, 12.9710], [77.5942, 12.9716], [77.5936, 12.9716], [77.5936, 12.9710]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.92,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 441.2,
                "perimeter_m": 84.0,
                "land_use": "residential",
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "parcel-103",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5942, 12.9710], [77.5949, 12.9710], [77.5949, 12.9716], [77.5942, 12.9716], [77.5942, 12.9710]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.95,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 514.8,
                "perimeter_m": 91.0,
                "land_use": "commercial",
                "metricCrs": "EPSG:32643"
            }
        },
        # P-104: Intentional overlap with P-105! Coordinates cross east into 77.5956
        {
            "type": "Feature",
            "id": "parcel-104",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5949, 12.9710], [77.5956, 12.9710], [77.5956, 12.9716], [77.5949, 12.9716], [77.5949, 12.9710]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.86,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 514.8,
                "perimeter_m": 91.0,
                "land_use": "residential",
                "metricCrs": "EPSG:32643"
            }
        },
        # P-105: Starts at 77.59545 (overlapping P-104 east portion by ~16.5 meters x 66 meters = ~8 m2 overlap)
        {
            "type": "Feature",
            "id": "parcel-105",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.59545, 12.9710], [77.5962, 12.9710], [77.5962, 12.9716], [77.59545, 12.9716], [77.59545, 12.9710]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.88,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 551.5,
                "perimeter_m": 94.0,
                "land_use": "residential",
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "parcel-106",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5930, 12.9718], [77.5937, 12.9718], [77.5937, 12.9725], [77.5930, 12.9725], [77.5930, 12.9718]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.93,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 565.0,
                "perimeter_m": 95.2,
                "land_use": "residential",
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "parcel-107",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5937, 12.9718], [77.5945, 12.9718], [77.5945, 12.9725], [77.5937, 12.9725], [77.5937, 12.9718]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.91,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 646.0,
                "perimeter_m": 102.0,
                "land_use": "residential",
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "parcel-108",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5945, 12.9718], [77.5953, 12.9718], [77.5953, 12.9725], [77.5945, 12.9725], [77.5945, 12.9718]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.90,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 646.0,
                "perimeter_m": 102.0,
                "land_use": "residential",
                "metricCrs": "EPSG:32643"
            }
        },
        # P-112: Suspicious tiny sliver polygon (< 2.0 m2)
        {
            "type": "Feature",
            "id": "parcel-112",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.59368, 12.97178], [77.59371, 12.97178], [77.59371, 12.97182], [77.59368, 12.97182], [77.59368, 12.97178]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.65,
                "confidenceType": "heuristic",
                "status": "review",
                "edited": False,
                "verified": False,
                "verifierId": None,
                "verifiedAt": None,
                "editHistory": [],
                "area_m2": 1.4,
                "perimeter_m": 5.8,
                "land_use": "unclassified",
                "metricCrs": "EPSG:32643"
            }
        }
    ]
}

with open("fixtures/geojson/parcels_detected.geojson", "w") as f:
    json.dump(parcels, f, indent=2)

# 2. BUILDINGS DETECTED
buildings = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [
        {
            "type": "Feature",
            "id": "bldg-201",
            "featureType": "building",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5931, 12.9711], [77.5935, 12.9711], [77.5935, 12.9715], [77.5931, 12.9715], [77.5931, 12.9711]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.93,
                "confidenceType": "heuristic",
                "status": "detected",
                "edited": False,
                "verified": False,
                "area_m2": 196.0,
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "bldg-202",
            "featureType": "building",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5937, 12.9711], [77.5941, 12.9711], [77.5941, 12.9715], [77.5937, 12.9715], [77.5937, 12.9711]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.91,
                "confidenceType": "heuristic",
                "status": "detected",
                "edited": False,
                "verified": False,
                "area_m2": 196.0,
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "bldg-203",
            "featureType": "building",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5943, 12.9711], [77.5948, 12.9711], [77.5948, 12.9715], [77.5943, 12.9715], [77.5943, 12.9711]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.95,
                "confidenceType": "heuristic",
                "status": "detected",
                "edited": False,
                "verified": False,
                "area_m2": 245.0,
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "bldg-204",
            "featureType": "building",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5950, 12.9711], [77.5954, 12.9711], [77.5954, 12.9715], [77.5950, 12.9715], [77.5950, 12.9711]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.89,
                "confidenceType": "heuristic",
                "status": "detected",
                "edited": False,
                "verified": False,
                "area_m2": 196.0,
                "metricCrs": "EPSG:32643"
            }
        },
        {
            "type": "Feature",
            "id": "bldg-205",
            "featureType": "building",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5956, 12.9711], [77.5960, 12.9711], [77.5960, 12.9715], [77.5956, 12.9715], [77.5956, 12.9711]]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.90,
                "confidenceType": "heuristic",
                "status": "detected",
                "edited": False,
                "verified": False,
                "area_m2": 196.0,
                "metricCrs": "EPSG:32643"
            }
        }
    ]
}

with open("fixtures/geojson/buildings_detected.geojson", "w") as f:
    json.dump(buildings, f, indent=2)

# 3. ROADS DETECTED
roads = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [
        {
            "type": "Feature",
            "id": "road-301",
            "featureType": "road",
            "geometry": {
                "type": "LineString",
                "coordinates": [[77.5925, 12.9708], [77.5965, 12.9708]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.91,
                "status": "detected",
                "name": "Main Access Corridor 1",
                "width_m": 8.0
            }
        },
        {
            "type": "Feature",
            "id": "road-302",
            "featureType": "road",
            "geometry": {
                "type": "LineString",
                "coordinates": [[77.5925, 12.9717], [77.5965, 12.9717]]
            },
            "properties": {
                "source": "ai",
                "sourceAssetId": "asset-ortho-001",
                "processingMode": "cv_baseline",
                "confidence": 0.89,
                "status": "detected",
                "name": "Residential Access Lane 2",
                "width_m": 6.0
            }
        }
    ]
}

with open("fixtures/geojson/roads_detected.geojson", "w") as f:
    json.dump(roads, f, indent=2)

# 4. GROUND TRUTH (Clean, official boundaries - P-104 and P-105 share exact boundary at 77.5955 with NO overlap)
ground_truth = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [
        {
            "type": "Feature",
            "id": "gt-parcel-104",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5949, 12.9710], [77.5955, 12.9710], [77.5955, 12.9716], [77.5949, 12.9716], [77.5949, 12.9710]]]
            },
            "properties": {
                "source": "ground_truth",
                "sourceAssetId": "asset-gt-001",
                "surveyNumber": "104/A",
                "registeredArea_m2": 441.2,
                "ownerType": "Private",
                "verified": True
            }
        },
        {
            "type": "Feature",
            "id": "gt-parcel-105",
            "featureType": "parcel",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.5955, 12.9710], [77.5962, 12.9710], [77.5962, 12.9716], [77.5955, 12.9716], [77.5955, 12.9710]]]
            },
            "properties": {
                "source": "ground_truth",
                "sourceAssetId": "asset-gt-001",
                "surveyNumber": "105/B",
                "registeredArea_m2": 514.8,
                "ownerType": "Private",
                "verified": True
            }
        }
    ]
}

with open("fixtures/geojson/ground_truth.geojson", "w") as f:
    json.dump(ground_truth, f, indent=2)

print("Generated all GeoJSON fixtures successfully!")
