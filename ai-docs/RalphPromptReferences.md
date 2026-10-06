---
title: "Ralph Prompt References"
summary: >-
  Starting reference list for writing Ralph prompts in this project: required
  docs to cite (including the shared machine-wide Python standards), the Ralph
  helper command line, and reusable standards, verification, and safety
  clauses to paste into prompts.
created: 2026-06-11
updated: 2026-10-06
tags: [ralph, prompts, standards]
status: current
source_ref: "main @ bda8049"
audience: "Whoever writes the next Ralph prompt"
---

# Ralph Prompt References

Use this file as the starting reference list when writing Ralph prompts for the Chrome bookmark manager.

## Required Project References

Every Ralph prompt for implementation work should point to:

- [ChromeBookmarkProjectPhases.md](./ChromeBookmarkProjectPhases.md) for project phases and safety constraints.
- [/mnt/shared/standards/python/README.md](/mnt/shared/standards/python/README.md) for machine-wide Python standards.
- [PythonEngineeringStandards.md](./PythonEngineeringStandards.md) for this project's Python standards addendum.
- [ChromeBookMarkFeature.md](./ChromeBookMarkFeature.md) as the original source document.

## Ralph Helper Configuration

Run Ralph from the repository root and point to the shared helper files with absolute paths:

```bash
ralph \
  -c /home/jeremy/work/ralph-helpers/ralph.yml \
  -H /home/jeremy/work/ralph-helpers/hats/code-assist.yml \
  run \
  -P /absolute/path/to/project/ai-docs/ralph-prompts/<prompt-file>.md
```

For this project, replace the prompt path with an absolute path under `/home/jeremy/src/chrome-bookmark-manager/ai-docs/ralph-prompts/`.

## Standard Ralph Prompt Clause

Add this clause to implementation prompts:

```markdown
## Project Standards

Read and follow:
- `ai-docs/ChromeBookmarkProjectPhases.md`
- `/mnt/shared/standards/python/README.md`
- `ai-docs/PythonEngineeringStandards.md`
- `ai-docs/ChromeBookMarkFeature.md`

Follow `/mnt/shared/standards/python/README.md` as the machine-wide Python source of truth and `ai-docs/PythonEngineeringStandards.md` as the project-specific addendum. If Git is not initialized, initialize it. Do not commit on `main` or `master`; create a feature branch before committing implementation work.
```

## Verification Clause

Add this verification block unless a task has a narrower reason not to:

```markdown
## Verification

Run and report:
- `poetry run pytest`
- `poetry run pyright`
- `poetry run ruff check .`
- `poetry run ruff format --check .`

If the Poetry project has not been initialized yet, create the project configuration first and then run the equivalent checks through Poetry.
```

## Safety Clause For Bookmark Work

Add this clause to any prompt involving Chrome bookmark files:

```markdown
## Bookmark Safety

Do not modify the user's live Chrome profile data. Use fixtures or temporary copies for tests and smoke checks. Write operations require explicit backup, Chrome-running detection, and rollback behavior before they are allowed.
```
