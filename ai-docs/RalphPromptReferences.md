# Ralph Prompt References

Use this file as the starting reference list when writing Ralph prompts for the Chrome bookmark manager.

## Required Project References

Every Ralph prompt for implementation work should point to:

- [ChromeBookmarkProjectPhases.md](./ChromeBookmarkProjectPhases.md) for project phases and safety constraints.
- [PythonEngineeringStandards.md](./PythonEngineeringStandards.md) for Poetry, strict typing, Pydantic, linting, and testing standards.
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
- `ai-docs/PythonEngineeringStandards.md`
- `ai-docs/ChromeBookMarkFeature.md`

Use Poetry for the Python environment. Run Ralph from the repository root. Put Python implementation code under root-level `src/` using the standard Python `src` layout. Put public documentation under root-level `docs/`; keep internal AI planning docs under `ai-docs/`. Include `README.md`, `.gitignore`, `.gitattributes`, and `.env.example` when initializing the repository. `.gitignore` must ignore Python caches/build artifacts, virtual environments, local `.env` files, and local agent state such as `.ralph/`, `.agents/`, `.claude/`, and `.codex/`; `.env.example` must remain tracked. Keep Pyright strict, Ruff lint/format, and pytest as required verification gates. Use Pydantic at external data and MCP boundaries, but prefer plain typed internal code where runtime validation is not needed. Do not add type ignores, broad `Any`, casts, or lint suppressions just to silence tooling. Follow SOLID principles pragmatically: keep responsibilities separated, avoid redundant code, isolate platform-specific behavior, and do not add speculative abstractions. If Git is not initialized, initialize it. Do not commit on `main` or `master`; create a feature branch before committing implementation work.
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
