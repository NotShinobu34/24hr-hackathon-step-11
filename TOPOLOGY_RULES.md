# Topology Validation Rules

## Purpose

Topology validation identifies suspicious or invalid geometry before final export.

## P0 checks

### 1. Invalid geometry

Flag polygons failing geometry validity checks.

Example:
- broken ring
- malformed polygon

### 2. Self-intersection

Flag polygons whose boundaries intersect themselves.

### 3. Parcel overlap

For parcel layers:

```text
area(A ∩ B) > allowedTolerance
```

flag an overlap.

The tolerance must be configurable.

### 4. Duplicate geometry

Flag exact or near-identical duplicate features.

### 5. Suspicious sliver

Flag polygons below a configurable area threshold.

Do not assume one universal threshold for every dataset.

## P1 checks

### 6. Gap

Where a project defines expected coverage, identify suspicious uncovered regions.

### 7. Building/parcel relationship

Flag buildings falling outside expected parcel boundaries when the data model supports this interpretation.

Do not automatically call this an error in all urban contexts.

### 8. Road/parcel relationship

Flag suspicious intersections only when business rules justify them.

## Issue object

```json
{
  "id": "issue-001",
  "featureId": "parcel-104",
  "relatedFeatureId": "parcel-105",
  "issueType": "overlap",
  "severity": "high",
  "message": "Possible overlap detected between parcel-104 and parcel-105.",
  "resolved": false
}
```

## Validation behavior

The validator should:
1. inspect a predictable set of rules
2. collect all issues
3. return machine-readable issues
4. never mutate user geometry silently

## Human review

Topology validation is advisory for the prototype.

The user may:
- inspect
- edit
- verify
- reject the issue

Do not automatically declare a legal boundary invalid.
