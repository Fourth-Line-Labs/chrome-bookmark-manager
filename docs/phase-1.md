---
title: "Phase 1 Read-Only Bookmark Audit"
summary: >-
  Public overview of Phase 1: a read-only CLI and stdio MCP server that
  discover Chrome/Chromium bookmark files on Windows, Linux, and macOS,
  validate the Bookmarks JSON with Pydantic, and render a Markdown outline.
  Describes each module's role (discovery, models, errors, parser, renderer,
  logging_setup, cli, mcp_server) and the read-only constraint.
created: 2026-06-11
updated: 2026-10-18
tags: [phase-1, architecture, cli, mcp]
status: current
source_ref: "main @ 9b45a6f"
---

# Phase 1 Read-Only Bookmark Audit

Phase 1 provides a safe command-line audit path for Chrome and Chromium
bookmarks. The tool can discover common profile bookmark files across Windows,
Linux, and macOS path shapes, validate a Chrome `Bookmarks` JSON file, and
produce a Markdown outline that preserves folder nesting. The same read-only
capabilities are available to AI clients through an MCP server.

## Architecture

- `discovery` finds existing bookmark candidates for the current platform,
  home directory, and process environment. Each of those inputs can be
  injected, so tests never depend on the real machine.
- `models` holds the Pydantic models that validate Chrome bookmark JSON at the
  external file boundary, plus the `BookmarkCandidate` value object returned by
  discovery.
- `errors` defines `BookmarkParseError` and its subclasses for bookmark files
  that are missing, not regular files, too large, unreadable, not UTF-8,
  malformed, or schema-invalid.
- `parser` loads a bookmark file and raises those errors with clear messages.
  It rejects directories and special files before opening them, and reads at
  most 64 MiB, so a bad path fails fast instead of hanging or exhausting
  memory.
- `renderer` converts validated bookmark data into Markdown.
- `logging_setup` sends package logs to stderr and a rotating debug log file
  in the platform's log directory.
- `cli` adapts command-line arguments to those boundaries.
- `mcp_server` exposes discovery, parsing, and rendering as read-only MCP
  tools over stdio. Under stdio, stdout carries the protocol itself, so the
  server logs only to stderr and the log file.

## Read-Only Constraint

The implementation reads bookmark files and writes only user-requested Markdown
output. It does not modify Chrome profile directories or bookmark JSON files.
