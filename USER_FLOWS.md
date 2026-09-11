# User Flows

## Flow 1 — Create survey project

```text
Home
 ↓
Open Survey Workspace
 ↓
Create Project
 ↓
Project Name
 ↓
Workspace
```

Success:
- project opens
- project status is visible

Failure:
- validation error
- retry option

## Flow 2 — Load imagery

```text
Workspace
 ↓
Add Source
 ↓
Choose ORI/drone image
 ↓
Preview metadata
 ↓
Load
 ↓
Map displays imagery
```

User should see:
- asset name
- asset type
- CRS if available
- image dimensions if available

## Flow 3 — Run extraction

```text
Imagery
 ↓
Run AI Extraction
 ↓
Processing
 ↓
Parcel / Building / Road layers
 ↓
Confidence summary
```

Never display a fake success result after an actual processing error.

## Flow 4 — Review topology issue

```text
Validation
 ↓
Issue detected
 ↓
Review Queue
 ↓
Select issue
 ↓
Map zooms to geometry
 ↓
Inspect feature metadata
```

## Flow 5 — Correct geometry

```text
Select feature
 ↓
Edit
 ↓
Move/add/delete vertex where supported
 ↓
Save
 ↓
Revalidate
 ↓
Issue resolved
```

## Flow 6 — Ground truth comparison

```text
Layers
 ↓
Enable Ground Truth
 ↓
Adjust opacity / comparison mode
 ↓
Inspect corresponding feature
```

## Flow 7 — Verification

```text
Feature review
 ↓
Verified / Needs Edit / Rejected
 ↓
Optional note
 ↓
Status saved
```

## Flow 8 — Export

```text
Export
 ↓
Choose layers
 ↓
Choose GeoJSON
 ↓
Validate
 ↓
Generate
 ↓
Download
```

## Flow 9 — Failure handling

Any major operation should support:

```text
loading
success
empty
failure
retry
```

Do not leave users on infinite loading screens.

## Demo flow

The recommended judge demo:

1. Open prepared survey project.
2. Show raw imagery.
3. Run extraction.
4. Reveal three layers.
5. Show counts/confidence.
6. Open topology issue.
7. Zoom to issue.
8. Edit parcel boundary.
9. Validate again.
10. Compare ground truth.
11. Mark feature verified.
12. Export GIS data.
