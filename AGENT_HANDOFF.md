# Agent Handoff Protocol

Every agent must leave the repository in a state another teammate can understand.

## Before starting

Read:
- relevant specs
- existing code
- current Git branch
- recent commits

## Before editing

Write down:
- goal
- files likely to change
- API/type impact
- tests needed

## After editing

Report:

```text
DONE
- ...

FILES CHANGED
- ...

API/TYPE CHANGES
- ...

TESTS
- ...

KNOWN LIMITATIONS
- ...

NEXT TEAM DEPENDENCY
- ...
```

## Shared contract changes

If you must change:
- GeoJSON feature contract
- endpoint
- database/data model
- geometry semantics

update the corresponding `.md` file in the same change and notify the team.

## Blocked task

Do not stay blocked silently.

Report:
- what failed
- what was expected
- what information is missing
- safe fallback

Then move to an independent task.
