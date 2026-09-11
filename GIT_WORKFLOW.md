# Git and Team Workflow

## Main branch

`main` must always be in a runnable state.

Never use `main` as a scratchpad.

## Branches

Preferred:

```text
feat/webgis
feat/geoai
feat/gis-engine
feat/topology
feat/export
feat/review
feat/seo
fix/mobile
fix/integration
```

## Pull requests

Each PR should:
- have one coherent purpose
- include tests where appropriate
- describe changed files
- identify integration risks

## Commit examples

```text
feat: add parcel GeoJSON layer
feat: implement extraction job endpoint
feat: add topology overlap check
fix: preserve polygon selection after refresh
fix: prevent invalid export
seo: add sitemap and page metadata
perf: reduce feature payload size
```

## Team rule

Do not create a massive `frontend` branch and a massive `backend` branch and wait until the end to merge.

Prefer feature branches and early integration.

## Conflict rule

If a merge conflict affects:
- API contract
- shared types
- geometry structures
- core map state

stop and resolve intentionally.

Do not accept an arbitrary auto-merge without reviewing semantics.

## Synchronization rhythm

At least at major milestones:

```text
commit
→ PR
→ review
→ merge
→ everyone pulls
→ continue
```

## Ownership

You = architecture/integration/WebGIS
Member 2 = GeoAI/CV
Member 3 = GIS backend/topology/export
Member 4 = UX/QA/SEO
