---
title: "Python Engineering Standards (Project Addendum)"
summary: >-
  Pointer to the machine-wide Python standards at
  /mnt/shared/standards/python/README.md plus the Chrome Bookmark Manager
  addendum: src layout, Pydantic at the Chrome JSON boundary, read-only
  bookmark access until backup/rollback exist, and the line Ralph prompts must
  include.
created: 2026-06-11
updated: 2026-10-06
tags: [python, standards, ralph]
status: current
source_ref: "main @ bda8049"
audience: "Humans and coding agents (Ralph) working in this repo"
---

# Python Engineering Standards

The machine-wide Python engineering standards live here:

[/mnt/shared/standards/python/README.md](/mnt/shared/standards/python/README.md)

Read and follow that file for Python project layout, Poetry, strict typing, Pydantic usage, Ruff, pytest, Git workflow, repository metadata, and safety expectations.

This file exists only as the Chrome Bookmark Manager project pointer plus project-specific addendum. Do not duplicate the shared standard here.

## Project Addendum

For this project:

- Use Python for the MCP server and local bookmark-processing logic.
- Keep implementation code under `src/chrome_bookmark_manager/`.
- Keep public project documentation under `docs/`.
- Keep internal AI/Ralph planning documents under `ai-docs/`.
- Use Pydantic for Chrome `Bookmarks` JSON input and future MCP tool input/output schemas.
- Keep bookmark inspection read-only until backup, lock detection, and rollback behavior exist.
- Do not modify live Chrome bookmark files during Phase 1.
- Treat Chrome Sync conflicts as a real data-loss risk.

## Ralph Prompt Requirement

Every Ralph implementation prompt for this project should reference the shared standard and this addendum.

Use this line in Ralph prompts:

> Follow `/mnt/shared/standards/python/README.md` as the machine-wide Python source of truth and `ai-docs/PythonEngineeringStandards.md` as the project-specific addendum.

This is the same sentence used in the Standard Ralph Prompt Clause in [RalphPromptReferences.md](./RalphPromptReferences.md); keep the two identical.
