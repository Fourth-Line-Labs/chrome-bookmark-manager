# Python Engineering Standards

This project uses Python for the MCP server and local bookmark-processing logic because it fits the MCP Python SDK, local JSON/file workflows, scraping, embeddings, and ChromaDB ecosystem.

Python is acceptable only with strict engineering guardrails. The goal is to keep the codebase type-safe, linted, testable, and explicit.

## Architecture Principles

- Follow SOLID principles pragmatically.
- Keep modules focused on one clear responsibility.
- Use the standard Python `src` layout for application code.
- Keep implementation code under root-level `src/`, with the importable package under a valid Python package name such as `src/chrome_bookmark_manager/`.
- Keep public documentation under root-level `docs/`.
- Keep internal AI planning/reference documents under `ai-docs/` unless they are intentionally promoted to public project docs.
- Do not add an extra wrapper directory such as `app/src/` or `project/src/` unless the repository becomes a monorepo with multiple packages.
- Separate external concerns from core logic:
  - file discovery
  - JSON loading and validation
  - bookmark domain models
  - Markdown rendering
  - CLI/MCP adapters
- Avoid duplicate logic. Extract shared behavior when duplication is real, not hypothetical.
- Prefer small composable functions and classes over large procedural scripts.
- Depend on abstractions at boundaries when they make testing or future replacement easier.
- Do not add layers, factories, or generic frameworks before the code needs them.
- Make future change easy by keeping boundaries explicit and names honest.
- Keep unsafe or platform-specific behavior isolated behind narrow interfaces.

## Environment

- Use Poetry for dependency management and packaging.
- Target Python 3.12 or newer unless a dependency forces a different choice.
- Commit both `pyproject.toml` and `poetry.lock` once the project is initialized.
- Keep runtime dependencies separate from development dependencies.
- Include public repository basics when initializing implementation:
  - `README.md`
  - `.gitignore`
  - `.gitattributes`
  - `.env.example` when environment variables are expected or likely
  - `docs/` for user-facing or contributor-facing documentation

`.gitignore` should include Python build/cache artifacts, virtual environments, local `.env` files, and local agent/orchestrator state such as `.ralph/`, `.agents/`, `.claude/`, and `.codex/`. Keep `.env.example` tracked so contributors can see expected configuration names without secrets.

Expected development toolchain:

- `pytest` for tests.
- `pytest-cov` for coverage when coverage tracking is added.
- `pyright` in strict mode for static type checking.
- `ruff` for linting and formatting.

## Git Workflow

- Ralph and other coding agents should run from the repository root.
- If the repository is not initialized, initialize it with Git before implementation.
- Do not commit code directly on `main` or `master`.
- Create a feature branch before committing implementation work.
- Work may be performed while currently on `main`, but commits must land on a separate branch.
- Verify the current branch before any commit.

## Type Safety

- Treat type checking as a required quality gate, not an optional warning system.
- Do not add `# type: ignore`, `Any`, casts, or broad suppressions just to get around an error.
- Prefer fixing the model, type signature, control flow, or validation boundary.
- If a third-party library has incomplete or wrong types, isolate that library behind a small typed wrapper.
- If needed, add local stubs or narrow adapter functions instead of weakening application code.
- Keep public functions and methods explicitly typed.
- Avoid implicit untyped dictionaries once data crosses into application logic.

Use Pydantic and Pyright for different jobs:

- Pyright catches mistakes in our code before runtime.
- Pydantic validates external data at runtime.

## Pydantic Usage

Use Pydantic at external boundaries:

- Chrome `Bookmarks` JSON input.
- CLI configuration input when needed.
- MCP tool input and output schemas.
- Future API or extension message boundaries.

Do not use Pydantic for every small internal object. Internal computed structures can be plain typed functions, dataclasses, or simple classes when no runtime validation is needed.

Preferred split:

- External data and tool/API boundaries: Pydantic models.
- Internal pure logic: dataclasses or plain typed code.

## Linting And Formatting

- Ruff linting must pass before work is considered complete.
- Ruff formatting must be applied consistently.
- Do not disable lint rules casually.
- If a lint rule is wrong for the project, document the reason in `pyproject.toml` comments or a project doc before changing it.

## Testing

- Write tests for parsing, validation, rendering, and error handling.
- Use fixture bookmark files and temporary directories.
- Do not test against the user's live Chrome profile by default.
- Any code that can modify bookmarks must first be proven against fixtures or temporary copies.

## Bookmark Safety

- Start with read-only bookmark inspection.
- Do not modify live Chrome bookmark files until backup, lock detection, and rollback behavior exist.
- Treat Chrome Sync conflicts as a real data-loss risk.
- Any write path must be explicit, tested, and guarded.

## Ralph Prompt Requirement

Every Ralph implementation prompt for this project should reference this file and require Ralph to follow it.

Use this line in Ralph prompts:

> Follow the project engineering standards in `ai-docs/PythonEngineeringStandards.md`.
