# Chrome Bookmark Manager

Chrome Bookmark Manager is a local-first Python tool for auditing Chrome and
Chromium bookmark files. Phase 1 is intentionally read-only: it discovers
bookmark files, parses Chrome's `Bookmarks` JSON, and renders the bookmark tree
as Markdown for review.

## Safety Status

This phase never writes to Chrome profile data. It does not edit, delete, back
up, lock, or reorganize live bookmark files.

## Install

```bash
poetry install
```

## Usage

List bookmark files found for common Chrome and Chromium profiles:

```bash
poetry run chrome-bookmark-manager --list-discovered
```

Render an explicit Chrome `Bookmarks` file to Markdown:

```bash
poetry run chrome-bookmark-manager \
  --bookmarks-file /path/to/Bookmarks \
  --output bookmarks.md
```

## Engineering Standards

This project follows a shared Python engineering standard (Poetry, strict
Pyright, Ruff, pytest, Pydantic at boundaries, Git workflow). It currently
lives outside this repository, on the development machine at:

```text
/mnt/shared/standards/python/README.md
```

Project-specific additions are in
[`ai-docs/PythonEngineeringStandards.md`](ai-docs/PythonEngineeringStandards.md).

If you cloned this repository somewhere else, that path will not exist.
[Issue #1](https://github.com/Fourth-Line-Labs/chrome-bookmark-manager/issues/1)
tracks moving the shared standards into their own repository so they are
available everywhere.

## Verification

```bash
poetry run pytest
poetry run pyright
poetry run ruff check .
poetry run ruff format --check .
```
