# UI Specification

## Design direction

The product should feel like a modern professional GIS workstation.

Influences:
- professional mapping tools
- modern data applications
- field-survey software
- restrained AI tooling

Avoid:
- generic AI SaaS landing pages
- excessive glassmorphism
- giant decorative gradients
- meaningless particles
- excessive cards
- flashy effects over map usability

## Layout

Desktop:

```text
┌────────────────────────────────────────────────────────────┐
│ Top Bar: Project · Status · Save · Export                 │
├──────────────┬───────────────────────────────┬─────────────┤
│ Left Tools   │                               │ Right Panel │
│              │             MAP               │             │
│ Layers       │       imagery + vectors       │ AI          │
│ Tools        │                               │ Validation  │
│ Sources      │                               │ Selection   │
│              │                               │ Review      │
└──────────────┴───────────────────────────────┴─────────────┘
```

## Primary map layers

1. Source imagery
2. Parcel candidates
3. Building footprints
4. Roads/access
5. Ground truth
6. Validation issues
7. Optional land-use

## Layer styling

The visual distinction between layers must be obvious without relying only on color.

Use:
- fill opacity
- line width
- selection outline
- patterns/icons where appropriate
- legend

## Feature panel

When a user selects a feature:

```text
Parcel P-104
Type: Parcel
Confidence: 94%
Source: AI
Status: Review

Area: 218.6 m²
Land use: Residential

Topology
⚠ Overlap with P-105

[Review Issue]
[Edit Geometry]
[Mark Verified]
```

## AI extraction panel

```text
AI EXTRACTION

Source: survey-001.tif

Features
✓ Parcels
✓ Buildings
✓ Roads

Confidence
Parcels     94%
Buildings   91%
Roads       88%

[Run Extraction]
```

During processing:

```text
Preparing imagery
██████████░░░░
Detecting features...
```

## Review queue

Prioritize:
1. high-severity topology issues
2. low-confidence features
3. features with ground-truth disagreement

## Status indicators

Use semantic text + icon, not color alone:

```text
Detected
Needs Review
Corrected
Verified
Invalid
```

## Responsive behavior

Mobile is secondary because GIS editing is desktop-first.

Still ensure:
- dashboard panels can stack
- map remains usable
- controls are touch-friendly
- no horizontal overflow
- important information remains accessible

## Accessibility

- keyboard-focusable controls
- labels on all inputs
- visible focus state
- meaningful ARIA labels where needed
- sufficient contrast
- text alternatives for status/notifications

## Loading/error/empty states

Every major panel needs:
- loading
- empty
- failure
- retry

## Microinteractions

Allowed:
- smooth map fly-to
- subtle layer transitions
- validation success state
- extraction progress

Avoid:
- animation that delays task completion
- decorative motion over dense map content
