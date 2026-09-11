# AI / Computer Vision Pipeline

## Goal

Extract preliminary candidates for:

1. parcels
2. buildings
3. roads/access corridors

## Key principle

Do not train a new custom deep-learning model from scratch during the initial practice implementation.

Use:
- pretrained/inference-ready models when available
- controlled computer-vision methods
- prepared sample output as a fallback

## Pipeline

```text
Input Raster
 ↓
Read metadata / CRS
 ↓
Preprocess
 ↓
Feature inference
 ↓
Masks / detections
 ↓
Post-process
 ↓
Vectorize
 ↓
Assign confidence
 ↓
GeoJSON
```

## Parcel pipeline

Potential baseline:
- image normalization
- edge/region cues
- segmentation/detection output
- contour extraction
- polygon approximation
- cleanup
- confidence assignment

## Building pipeline

Potential baseline:
- object/region detection
- connected components/contours
- polygon simplification
- confidence

## Road pipeline

Potential baseline:
- segmentation/detection
- morphological cleanup
- line/area extraction
- graph/line simplification where appropriate

## Confidence

Confidence must represent model/pipeline confidence or a transparent heuristic.

Never fabricate scientific confidence values.

If confidence is heuristic, label it internally as heuristic and explain the basis.

## Output contract

Each feature should include:

```json
{
  "id": "building-001",
  "featureType": "building",
  "geometry": {},
  "properties": {
    "confidence": 0.91,
    "source": "ai",
    "status": "review"
  }
}
```

## Failure/fallback

If extraction fails:
- return explicit failure
- preserve previous results
- offer retry
- support a prepared demo fixture

The UI must never imply real inference occurred when it did not.

## Model boundary

The model must not directly decide legal cadastral truth.

It produces **candidate features**.

The GIS validation and human-review layers remain authoritative for the prototype workflow.
