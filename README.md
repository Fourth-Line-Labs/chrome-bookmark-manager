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

## Logging

Every run that gets past argument parsing writes a debug log, so there is a
record to inspect when something goes wrong. Argument errors such as an unknown
flag are reported on the console only. If the log location cannot be written,
the tool prints a `File logging disabled` warning and continues with console
output only. The log file rotates at 1 MB and keeps three old copies.

| Platform | Default log file |
| --- | --- |
| Linux | `~/.local/state/chrome-bookmark-manager/log/chrome-bookmark-manager.log` |
| macOS | `~/Library/Logs/chrome-bookmark-manager/chrome-bookmark-manager.log` |
| Windows | `%LOCALAPPDATA%\chrome-bookmark-manager\Logs\chrome-bookmark-manager.log` |

- `-v` prints info messages to stderr, and `-vv` prints debug messages. They
  never go to stdout, so piping Markdown output stays clean.
- `CHROME_BOOKMARK_MANAGER_LOG_DIR` sets the log **directory**, and
  `chrome-bookmark-manager.log` is created inside it.
- `--log-file PATH` sets the full log **file** path. If both are set,
  `--log-file` wins.
- The log is meant for one run at a time. If several runs overlap, rotation of
  the shared file can lose or misplace records, so give each concurrent run its
  own `--log-file`.
- An unexpected failure prints the log file path. Attach that file when you
  report a problem.

Logs record file paths, counts, and errors. Regular log messages never include
bookmark names or URLs, and validation errors are configured not to echo the
input. One exception: the traceback for an unexpected failure includes the
exception's own message, which in rare cases (such as a text-encoding error) can
quote a single character from a bookmark.

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
