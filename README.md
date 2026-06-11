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

## Verification

```bash
poetry run pytest
poetry run pyright
poetry run ruff check .
poetry run ruff format --check .
```
