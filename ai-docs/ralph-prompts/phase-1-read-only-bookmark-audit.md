# Ralph Prompt: Phase 1 Read-Only Bookmark Audit

Use this prompt with Ralph `code-assist` for the first implementation slice.

Suggested command:

```bash
ralph \
  -c /home/jeremy/work/ralph-helpers/ralph.yml \
  -H /home/jeremy/work/ralph-helpers/hats/code-assist.yml \
  run \
  -P /home/jeremy/src/chrome-bookmark-manager/ai-docs/ralph-prompts/phase-1-read-only-bookmark-audit.md
```

Run this from the repository root: `/home/jeremy/src/chrome-bookmark-manager`.

## Task: Phase 1 Read-Only Bookmark Audit

## Objective

Create the first safe implementation slice for the Chrome bookmark manager: a Poetry-managed, strictly typed Python project using the standard `src` layout that can discover Chrome/Chromium bookmark files across Windows, Linux, and macOS, parse a Chrome `Bookmarks` JSON file, and render a Markdown bookmark tree.

This slice must be read-only. Do not implement write/reorganization behavior yet.

## Project References

Read and follow:

- `ai-docs/ChromeBookmarkProjectPhases.md`
- `ai-docs/PythonEngineeringStandards.md`
- `ai-docs/ChromeBookMarkFeature.md`
- `ai-docs/RalphPromptReferences.md`

Use Poetry for the Python environment. Run Ralph from the repository root. Put Python implementation code under root-level `src/` using the standard Python `src` layout. Put public documentation under root-level `docs/`; keep internal AI planning docs under `ai-docs/`. Include `README.md`, `.gitignore`, `.gitattributes`, and `.env.example` when initializing the repository. `.gitignore` must ignore Python caches/build artifacts, virtual environments, local `.env` files, and local agent state such as `.ralph/`, `.agents/`, `.claude/`, and `.codex/`; `.env.example` must remain tracked. Keep Pyright strict, Ruff lint/format, and pytest as required verification gates. Use Pydantic at external data and MCP boundaries, but prefer plain typed internal code where runtime validation is not needed. Do not add type ignores, broad `Any`, casts, or lint suppressions just to silence tooling. Follow SOLID principles pragmatically: keep responsibilities separated, avoid redundant code, isolate platform-specific behavior, and do not add speculative abstractions.

## Git Workflow

This repository may not have Git initialized yet.

1. At the start of the run, check whether the repository root has Git initialized.
2. If Git is not initialized, run `git init`.
3. Do not commit implementation work on `main` or `master`.
4. Create and switch to a feature branch before committing. Use a branch name such as `feature/phase-1-read-only-bookmark-audit`.
5. Before any commit, run `git branch --show-current` and verify the current branch is not `main` or `master`.
6. If Ralph creates commits, the commits must be on the feature branch.

## Context

This repository currently contains planning docs only. Phase 1 from the project plan is the "Audit & Clean MVP": read the local Chrome `Bookmarks` JSON file and produce a human-readable Markdown map of the bookmark folder structure.

The user primarily expects this app to run on Windows, but development is happening on an Ubuntu VM. Cross-platform bookmark discovery must be designed from the start.

Terminology:

- A Pydantic model is a class that validates structured data.
- A fixture is sample test data or reusable test setup.
- A test fixture file is sample JSON under a test directory, such as `tests/fixtures/bookmarks/simple_bookmarks.json`.
- A pytest fixture is a function decorated with `@pytest.fixture`.

## Requirements

1. Initialize Git if it is not already initialized.
2. Create and use a feature branch before committing any work.
3. Initialize a Poetry Python project if one does not already exist.
4. Configure Python 3.12 or newer, Pyright strict mode, Ruff linting/formatting, and pytest.
5. Use the standard public Python project layout:
   - project root contains `README.md`, `.gitignore`, `.gitattributes`, `.env.example`, `pyproject.toml`, and `poetry.lock`
   - public documentation lives under root-level `docs/`
   - internal AI planning/reference docs remain under `ai-docs/`
   - Python package code lives under `src/chrome_bookmark_manager/`
   - tests live under `tests/`
6. Add a concise `README.md` suitable for a future public repository. It should explain what the project is, current Phase 1 scope, install/test commands, and safety status.
7. Add an appropriate Python `.gitignore`. It must include:
   - Python caches and build outputs such as `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.pyright/`, `dist/`, `build/`, and `*.egg-info/`
   - virtual environments such as `.venv/` and `venv/`
   - local environment files such as `.env`, `.env.*`, but not `.env.example`
   - local agent/orchestrator state directories such as `.ralph/`, `.agents/`, `.claude/`, and `.codex/`
8. Add a `.gitattributes` file with sensible text normalization for a cross-platform project.
9. Add a tracked `.env.example` file showing expected environment variable names if any are needed now. If no environment variables are currently required, include a brief comment stating that no environment variables are required for Phase 1.
10. Add initial public docs under `docs/` for Phase 1 usage or architecture. Do not move `ai-docs/` content wholesale into `docs/`; summarize user-facing material only.
11. Create a small, logical package structure with separated responsibilities:
   - platform/profile bookmark discovery
   - JSON file loading
   - Pydantic validation models for Chrome bookmark JSON
   - internal typed representation if needed
   - Markdown rendering
   - CLI adapter
12. Implement a CLI that accepts:
   - `--bookmarks-file PATH` to parse an explicit Chrome `Bookmarks` file
   - `--output PATH` to write Markdown output
   - a discovery/list mode that reports candidate bookmark files found on the current machine
13. Implement read-only bookmark discovery for common Chrome and Chromium paths:
   - Windows:
     - `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks`
     - `%LOCALAPPDATA%\Google\Chrome\User Data\Profile 1\Bookmarks`
     - `%LOCALAPPDATA%\Chromium\User Data\Default\Bookmarks`
   - Linux:
     - `~/.config/google-chrome/Default/Bookmarks`
     - `~/.config/google-chrome/Profile 1/Bookmarks`
     - `~/.config/chromium/Default/Bookmarks`
   - macOS:
     - `~/Library/Application Support/Google/Chrome/Default/Bookmarks`
     - `~/Library/Application Support/Google/Chrome/Profile 1/Bookmarks`
     - `~/Library/Application Support/Chromium/Default/Bookmarks`
14. Discovery should return all candidate profiles that exist, not just the first match.
15. Discovery must be testable without depending on the real user's home directory or environment variables.
16. Parse Chrome bookmark folders and URL nodes recursively.
17. Render Markdown that preserves folder nesting and outputs URL bookmarks as links.
18. Handle missing files, malformed JSON, and invalid bookmark schema with clear errors.
19. Add test fixture files for representative bookmark structures, including:
    - simple bookmark bar
    - nested folders
    - other bookmarks/mobile roots if present
    - malformed JSON or invalid schema
20. Do not modify, delete, back up, rewrite, or lock the user's live Chrome bookmark files in this slice.

## Non-Goals

- Do not implement bookmark write operations.
- Do not kill Chrome or inspect running Chrome processes yet.
- Do not delete Chrome checksum fields or `.bak` files.
- Do not implement MCP server tools yet unless a minimal placeholder is required by project setup.
- Do not implement semantic search, crawling, embeddings, ChromaDB, or Chrome extension behavior.

## Architecture Expectations

Keep the implementation small but clean.

Prefer boundaries like:

- `discovery`: finds candidate bookmark files from injected environment/path inputs.
- `models`: Pydantic models for the Chrome bookmark JSON boundary.
- `parser`: loads and validates a bookmark file.
- `renderer`: converts validated bookmark data into Markdown.
- `cli`: handles command-line arguments and user-facing errors.

Place these modules under `src/chrome_bookmark_manager/` or an equivalent valid Python package name. Do not put application modules directly in the repository root. Do not create an extra wrapper directory above `src/` for a single-package project.

These names are suggestions, not a mandate. Follow the project standards and make the simplest logical architecture that satisfies the requirements.

## Bookmark Safety

Do not modify the user's live Chrome profile data. Use fixtures or temporary copies for tests and smoke checks. Write operations require explicit backup, Chrome-running detection, and rollback behavior before they are allowed, and they are outside this task.

## Success Criteria

- [ ] Poetry project exists with committed `pyproject.toml` and `poetry.lock`.
- [ ] Git is initialized if it was missing at the start.
- [ ] Implementation commits, if any, are on a feature branch, not `main` or `master`.
- [ ] Python implementation code lives under `src/chrome_bookmark_manager/` or an equivalent valid Python package under `src/`.
- [ ] Repository includes `README.md`, `.gitignore`, `.gitattributes`, `.env.example`, and public `docs/`.
- [ ] `.gitignore` ignores local Ralph/Codex/Claude/agent state and local `.env` files while keeping `.env.example` trackable.
- [ ] README includes current scope, safety status, installation, and verification commands.
- [ ] Public docs summarize Phase 1 usage or architecture without exposing internal-only planning details unnecessarily.
- [ ] CLI can parse an explicit fixture bookmark file and write a Markdown output file.
- [ ] CLI can list discovered bookmark candidate paths without modifying them.
- [ ] Discovery logic is covered for Windows, Linux, and macOS path shapes using injected test inputs.
- [ ] Parser validates Chrome bookmark JSON through Pydantic at the file boundary.
- [ ] Markdown output preserves folder nesting and bookmark URLs.
- [ ] Missing file, malformed JSON, and invalid schema paths have focused tests.
- [ ] Code is typed without broad `Any`, type ignores, casts, or suppressions added just to silence tooling.
- [ ] Architecture separates discovery, validation/parsing, rendering, and CLI concerns.

## Verification

Run and report:

- `poetry run pytest`
- `poetry run pyright`
- `poetry run ruff check .`
- `poetry run ruff format --check .`

Also run at least one CLI smoke test against a fixture file and report the command plus the resulting Markdown file path.

## Completion

Only emit `LOOP_COMPLETE` after all success criteria are met and verification evidence is recorded. If any verification command cannot run because of a missing system dependency, document the blocker clearly and keep the implementation in a state where the command should pass once the dependency is available.
