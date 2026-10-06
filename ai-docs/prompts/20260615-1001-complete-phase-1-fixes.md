---
title: "Prompt: Complete Phase 1 Fixes"
summary: >-
  Agent prompt for the Phase 1 review follow-up: make Windows bookmark
  discovery read LOCALAPPDATA from the real process environment when no env
  mapping is injected, add a test for it, and keep commits off main. Executed
  on branch chore/phase-1-cleanup.
created: 2026-06-15
updated: 2026-10-06
tags: [prompts, phase-1, bugfix, windows]
status: archived
source_ref: "main @ bda8049"
audience: "A coding agent picking up the Phase 1 fixes"
---

# Prompt: Complete Phase 1 Fixes

You are working in `/home/jeremy/src/chrome-bookmark-manager`.

This is a small completion task for Phase 1. Do only what is explicitly requested in this prompt. Do not implement Phase 2. Do not add semantic search, crawling, embeddings, ChromaDB, MCP tools, Chrome extension code, bookmark write operations, backup logic, or Chrome process/lock handling.

## Read First

Read these files before changing code:

- `/mnt/shared/standards/python/README.md`
- `ai-docs/ChromeBookmarkProjectPhases.md`
- `ai-docs/PythonEngineeringStandards.md`
- `README.md`
- `docs/phase-1.md`

These explain what we are building and the Python standards for this machine.

## Context

Phase 1 is the read-only Chrome bookmark audit slice. It should:

- discover Chrome/Chromium bookmark files across Windows, Linux, and macOS
- parse Chrome `Bookmarks` JSON through Pydantic validation
- render a Markdown bookmark tree
- remain strictly read-only against live browser profile data
- pass pytest, Pyright strict mode, and Ruff

The previous implementation mostly works, but the Phase 1 review found two blockers.

## Required Fixes

1. Fix Windows discovery when `env` is not injected.

   Current behavior: `discover_bookmark_files(platform="windows")` defaults `env` to `{}`, so Windows discovery returns no candidates unless tests inject `LOCALAPPDATA`.

   Required behavior: when `env` is omitted, discovery should use the real process environment. When `env` is explicitly provided, use that injected mapping exactly so tests remain deterministic.

   Keep the discovery logic testable without depending on the real user's home directory or real environment variables.

2. Add focused tests for the Windows default environment behavior.

   Add a test that proves `discover_bookmark_files(platform="windows", env omitted, ...)` reads `LOCALAPPDATA` from the process environment and still uses injected `path_exists`.

   Preserve existing tests for injected `env`.

3. Confirm Git workflow compliance for this fix.

   Do not commit on `main` or `master`.

   If you need to commit, create and switch to a feature branch first, such as:

   ```bash
   git switch -c fix/phase-1-windows-discovery
   ```

   Do not rewrite history, reset branches, or force-push. The earlier `main` commit is a process problem to note, not something to repair destructively in this task.

## Constraints

- Follow `/mnt/shared/standards/python/README.md`.
- Keep Pyright strict.
- Do not add `# type: ignore`, broad `Any`, casts, or lint suppressions just to silence tooling.
- Keep the implementation small and consistent with the current package structure.
- Do not modify live Chrome bookmark files.
- Do not touch unrelated files unless required by this task.
- Preserve existing user or agent changes in the worktree.

## Verification

Run and report:

```bash
poetry run pytest
poetry run pyright
poetry run ruff check .
poetry run ruff format --check .
```

Also run a CLI smoke check against the existing fixture file, for example:

```bash
poetry run chrome-bookmark-manager \
  --bookmarks-file tests/fixtures/bookmarks/simple_bookmarks.json \
  --output /tmp/chrome-bookmark-manager-phase-1-smoke.md
```

## Completion Criteria

This task is complete only when:

- Windows discovery uses the real process environment when `env` is omitted.
- Injected `env` behavior remains deterministic and covered.
- All verification commands pass.
- The CLI smoke check succeeds.
- No unrelated features or refactors were added.
- No commit was made on `main` or `master`.
