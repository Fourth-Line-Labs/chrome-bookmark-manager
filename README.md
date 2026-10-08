# Chrome Bookmark Manager

Chrome Bookmark Manager is a local-first Python tool for auditing Chrome and
Chromium bookmark files. Phase 1 is intentionally read-only: it discovers
bookmark files, parses Chrome's `Bookmarks` JSON, and renders the bookmark tree
as Markdown for review.

## Safety Status

This phase never writes to Chrome profile data. It does not edit, delete, back
up, lock, or reorganize live bookmark files.

## Install

For development, from a clone of this repository:

```bash
poetry install
```

## Try It Without Cloning

The repository is public, so any machine with **Python 3.12 or newer** can
install the tool into a throwaway virtual environment. Neither Git nor Poetry
is needed. Nothing is installed system-wide, and you can delete the
environment folder afterwards.

These steps install the **latest development version from `main`**, not a
tagged release, so two installs made on different days can behave differently.
When reporting a problem, say roughly when you installed.

Windows (PowerShell):

```powershell
py -3 -m venv $env:TEMP\cbm
& $env:TEMP\cbm\Scripts\pip install https://github.com/Fourth-Line-Labs/chrome-bookmark-manager/archive/refs/heads/main.zip

& $env:TEMP\cbm\Scripts\chrome-bookmark-manager -v --list-discovered
& $env:TEMP\cbm\Scripts\chrome-bookmark-manager -v `
    --bookmarks-file "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Bookmarks" `
    --output "$HOME\bookmarks.md"
```

`py -3` picks the newest Python 3 installed. If pip then reports that the
Python version is too old, install Python 3.12 or newer. If the `py` launcher
isn't available (for example with the Microsoft Store Python), use
`python -m venv $env:TEMP\cbm` instead.

macOS and Linux:

```bash
python3 -m venv /tmp/cbm
/tmp/cbm/bin/pip install https://github.com/Fourth-Line-Labs/chrome-bookmark-manager/archive/refs/heads/main.zip

/tmp/cbm/bin/chrome-bookmark-manager -v --list-discovered
/tmp/cbm/bin/chrome-bookmark-manager -v \
  --bookmarks-file "$HOME/Library/Application Support/Google/Chrome/Default/Bookmarks" \
  --output "$HOME/bookmarks.md"
```

On Linux the default Chrome file is
`~/.config/google-chrome/Default/Bookmarks`. On Debian and Ubuntu, `python3 -m
venv` needs the `python3-venv` package.

The tool only reads bookmark files, so it is safe to run while Chrome is open.

### Finding your bookmarks file

`--list-discovered` currently checks only Chrome's `Default` and `Profile 1`
profiles and Chromium's `Default` profile
([#5](https://github.com/Fourth-Line-Labs/chrome-bookmark-manager/issues/5)).
If your bookmarks are somewhere else, point `--bookmarks-file` at the file
directly:

- **Other Chrome profiles:** open `chrome://version` in Chrome. The
  *Profile Path* line shows the profile folder; the file is `Bookmarks` inside
  it.
- **Bookmarks saved to your Google Account** (without full Chrome Sync) are
  stored in a separate `AccountBookmarks` file in the same profile folder.
- **Microsoft Edge** uses the same format:
  `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Bookmarks` on Windows.

### Known limitations

- On Windows, printing Markdown to the console can fail when a bookmark name
  contains characters the console encoding can't represent, such as emoji
  ([#4](https://github.com/Fourth-Line-Labs/chrome-bookmark-manager/issues/4)).
  Use `--output` to write a file instead.

### Reporting a problem

Run the command again with `-v`, then attach the log file it names (see
[Logging](#logging)). If the output shows a `File logging disabled` warning,
there is no log file; copy the full console output instead.

Logs contain file paths, which include your username, but regular log messages
never include bookmark names or URLs. At most, the traceback for an unexpected
failure can quote a single character from a bookmark, as described under
[Logging](#logging). If the problem is in the Markdown output itself, describe
what looks wrong instead, because the log is designed not to show bookmark
content.

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
