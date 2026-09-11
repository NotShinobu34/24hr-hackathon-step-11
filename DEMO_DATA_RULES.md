# Demo Data & Presentation Rules

## Purpose

During hackathons and live evaluations, demonstrations frequently collapse due to transient network drops, heavy GPU cold starts, or unhandled image format quirks.

This document sets explicit, binding rules for how demo datasets are prepared, loaded, and presented.

---

## 1. Transparency & Integrity First

1. **Never Conceal Fallback**:
   - If an extraction request uses a pre-computed demo fixture or OpenCV fallback rather than a live deep learning model, the UI must explicitly display:
     `Mode: Demo Fixture` or `Mode: CV Baseline`.
   - Never show a spinner followed by simulated delays intended to mislead judges into thinking live deep-learning inference took place when it did not.
2. **Honest Confidence Scoring**:
   - Every confidence score must be accompanied by its methodology:
     - `model_probability`: Derived from neural network softmax/sigmoid activation.
     - `heuristic`: Derived from edge-contrast, gradient strength, and contour compactness.
     - `demo_fixture`: Derived from benchmark annotations.
   - Never fabricate scientific accuracy values (e.g. "99.98% cadastral precision").

---

## 2. Demo Dataset Requirements

The primary demo survey dataset must contain:

1. **Realistic Urban Density**:
   - High-resolution aerial orthophoto with recognizable features: building rooftops, parcel property lines (fences, walls, vegetation borders), and access corridors.
   - At least 20–30 recognizable candidate parcels in the viewport.
2. **Deterministic Topology Issues for Review Workflow**:
   - The demo dataset must contain exactly **1 high-severity overlap** between two adjacent parcels (e.g., `P-104` and `P-105`).
   - Exactly **1 low-confidence or sliver parcel** (e.g., `P-112`).
   - This ensures the judge directly sees:
     1. Issue detection on the map.
     2. Review queue item click.
     3. Smooth fly-to camera movement.
     4. Geometry vertex drag correction.
     5. Revalidation clearing the error.
3. **Aligned Ground-Truth Reference Layer**:
   - An official reference layer covering the same spatial extent, allowing the judge to evaluate how AI-assisted boundaries compare with ground truth via opacity slider or split-swipe.

---

## 3. Fast Failure & Fallback Protocol

```text
User clicks [Run Extraction]
         │
         ▼
Try Live Model Inference (timeout: 6s)
         │
    ┌────┴────────────────────────┐
    │                             │
 Success                       Failure / Timeout / No GPU
    │                             │
    ▼                             ▼
Render Live Predictions      Fallback to CV Baseline or Demo Fixture
Mode: "model_inference"      Show Notification: "Live model unavailable; loaded verified baseline"
                             Mode: "cv_baseline" | "demo_fixture"
```

The system will never leave the judge on an infinite loading spinner or crash with an unhandled exception.
