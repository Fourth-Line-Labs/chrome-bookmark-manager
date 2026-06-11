# Phase 1 Read-Only Bookmark Audit

Phase 1 provides a safe command-line audit path for Chrome and Chromium
bookmarks. The tool can discover common profile bookmark files across Windows,
Linux, and macOS path shapes, validate a Chrome `Bookmarks` JSON file, and
produce a Markdown outline that preserves folder nesting.

## Architecture

- `discovery` finds existing bookmark candidates from injected platform, home,
  and environment inputs.
- `models` validates Chrome bookmark JSON at the external file boundary with
  Pydantic.
- `parser` loads a bookmark file and reports missing, malformed, or invalid
  input clearly.
- `renderer` converts validated bookmark data into Markdown.
- `cli` adapts command-line arguments to those boundaries.

## Read-Only Constraint

The implementation reads bookmark files and writes only user-requested Markdown
output. It does not modify Chrome profile directories or bookmark JSON files.
