# Testing Strategy

## Testing pyramid

### Unit

Test:
- utility functions
- geometry rules
- confidence calculations
- API validation
- data transformations

### Integration

Test:
- API ↔ processing
- project creation
- extraction job
- feature retrieval
- validation
- edit/save
- export

### UI/E2E

Test:
- create/open project
- run extraction
- layer visibility
- feature selection
- issue review
- edit
- validate
- verify
- export

## P0 acceptance tests

### Test 1 — Map

Given a valid project,
when it opens,
the map and imagery render.

### Test 2 — Extraction

Given a valid source,
when extraction runs,
parcel/building/road outputs are returned or an explicit error is shown.

### Test 3 — Feature interaction

Given a detected feature,
when selected,
its details appear.

### Test 4 — Topology

Given two overlapping parcel fixtures,
validation returns an overlap issue.

### Test 5 — Correction

Given an invalid/overlapping test fixture,
after correction and save,
revalidation produces the expected result.

### Test 6 — Export

Given valid features,
export returns a valid GeoJSON FeatureCollection.

## Edge cases

Test:
- empty dataset
- malformed GeoJSON
- missing CRS
- unsupported file
- huge file
- extraction timeout/failure
- invalid geometry
- duplicate features
- API offline
- partial project data
- refresh during processing
- multiple edits before save

## Browser/device

At minimum:
- Chromium desktop
- one secondary desktop browser
- 1440px
- 1024px
- 768px
- 390px

## Performance

Check:
- initial load
- map responsiveness
- GeoJSON rendering
- image decoding
- extraction latency
- memory use for repeated layer updates

## Final test gate

Before submission:
1. clean install
2. build
3. lint
4. test
5. run production build
6. inspect console
7. inspect network errors
8. test production deployment
9. execute demo flow twice
