---
title: "Phase 1 Read-Only Bookmark Audit"
summary: >-
  Public overview of Phase 1: a read-only CLI that discovers Chrome/Chromium
  bookmark files on Windows, Linux, and macOS, validates the Bookmarks JSON
  with Pydantic, and renders a Markdown outline. Describes each module's role
  (discovery, models, errors, parser, renderer, cli) and the read-only
  constraint.
created: 2026-06-11
updated: 2026-10-06
tags: [phase-1, architecture, cli]
status: current
source_ref: "chore/phase-1-cleanup @ f654c35"
---

# Phase 1 Read-Only Bookmark Audit

Phase 1 provides a safe command-line audit path for Chrome and Chromium
bookmarks. The tool can discover common profile bookmark files across Windows,
Linux, and macOS path shapes, validate a Chrome `Bookmarks` JSON file, and
produce a Markdown outline that preserves folder nesting.

## Architecture

- `discovery` finds existing bookmark candidates for the current platform,
  home directory, and process environment. Each of those inputs can be
  injected, so tests never depend on the real machine.
- `models` holds the Pydantic models that validate Chrome bookmark JSON at the
  external file boundary, plus the `BookmarkCandidate` value object returned by
  discovery.
- `errors` defines `BookmarkParseError` and its subclasses for missing,
  malformed, and schema-invalid bookmark files.
- `parser` loads a bookmark file and raises those errors with clear messages.
- `renderer` converts validated bookmark data into Markdown.
- `cli` adapts command-line arguments to those boundaries.

## Read-Only Constraint

The implementation reads bookmark files and writes only user-requested Markdown
output. It does not modify Chrome profile directories or bookmark JSON files.
