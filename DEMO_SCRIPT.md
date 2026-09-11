# Demo Script

## Target demo length

3–5 minutes.

## Opening

“GeoParcel AI converts high-resolution urban imagery into preliminary cadastral intelligence that a surveyor can review, correct and export.”

## Step 1 — Source

Show survey project and imagery.

Explain:
“This is the source imagery for the survey area.”

## Step 2 — AI extraction

Click **Run AI Extraction**.

Show:
- parcel candidates
- building footprints
- roads/access

Explain:
“The system proposes preliminary features and attaches confidence so low-confidence results can be prioritized for review.”

## Step 3 — Quality control

Open validation.

Show:
“Rather than blindly accepting AI output, we run deterministic topology checks.”

Open an overlap issue.

## Step 4 — Human review

Map zooms to the issue.

Edit a boundary.

Explain:
“The surveyor remains in the loop.”

## Step 5 — Revalidation

Run validation again.

Show:
“After correction, the geometry is validated again.”

## Step 6 — Ground truth

Toggle reference data.

Explain:
“We can compare preliminary AI results with ground-truth/reference data.”

## Step 7 — Verification

Mark corrected feature as verified.

## Step 8 — Export

Export GeoJSON.

Closing:
“The goal is not to replace surveying. It is to reduce repetitive manual digitization and move surveyors toward a faster review-and-verify workflow.”

## Do not say

- “99.9% accurate”
- “fully autonomous cadastral mapping”
- “legally valid cadastral records”

unless such claims are genuinely supported by the implementation/evaluation.
