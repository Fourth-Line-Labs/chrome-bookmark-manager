---
title: "Chrome Bookmark Manager Project Phases"
summary: >-
  Compact reference for the three implementation phases: Phase 1 audit and
  clean MVP (read Chrome's Bookmarks JSON, render a Markdown tree), Phase 2
  semantic memory (crawl, embed, ChromaDB search), and Phase 3 live watcher
  (Chrome extension). Also lists cross-cutting safety constraints and links to
  the standards and Ralph prompt references.
created: 2026-06-11
updated: 2026-10-06
tags: [planning, phases, roadmap]
status: current
source_ref: "main @ bda8049"
---

# Chrome Bookmark Manager Project Phases

This file is a compact reference for the three major implementation phases in the Chrome bookmark manager project.

Source reference: [ChromeBookMarkFeature.md](./ChromeBookMarkFeature.md)

## Phase 1: Audit & Clean MVP

Build a standalone Python MCP server that reads the local Chrome `Bookmarks` JSON file and produces a human-readable map of the user's bookmark structure.

The main outcome is a master Markdown representation of the bookmark folder tree so the user can audit, clean up, and reorganize bookmarks through text.

Important implementation concerns:
- Locate and parse the Chrome profile's `Bookmarks` file.
- Start with safe read-only inspection before write operations.
- Handle Chrome file locking before any write path.
- Account for Chrome's bookmark checksum and `.bak` behavior during controlled writes.
- Verify changes against fixtures or temporary copies before touching live profile data.

## Phase 2: Semantic Memory

Add content-based bookmark search by crawling bookmarked URLs, extracting page text, summarizing or indexing the content, and storing vectors locally.

The main outcome is semantic search through natural language queries, even when the query terms do not appear in bookmark titles or folder names.

Candidate components:
- ChromaDB for local vector storage.
- Crawl4AI or BeautifulSoup for page text extraction.
- Local `sentence-transformers` embeddings by default, with optional API-based embeddings if explicitly configured.
- Background indexing for bookmarked URLs.

## Phase 3: Live Watcher

Add a lightweight Chrome extension that observes bookmark changes in real time and coordinates with the Python MCP server.

The main outcome is automatic synchronization and immediate indexing of new bookmarks.

Expected extension capabilities:
- Use Chrome bookmark listeners such as `chrome.bookmarks.onCreated`.
- Trigger indexing when new bookmarks are added.
- Optionally add omnibox integration, such as an `@find` keyword, to surface semantic search results from the browser address bar.

## Cross-Cutting Constraints

- Keep the architecture local-first.
- Protect user bookmark data and browsing history.
- Avoid destructive writes to live Chrome profile data without backups and explicit verification.
- Treat Chrome Sync conflicts as a real risk for write operations.
- Prefer incremental Ralph prompts that build one verifiable slice at a time.

## Related References

- [/mnt/shared/standards/python/README.md](/mnt/shared/standards/python/README.md) defines the machine-wide Python, Poetry, typing, Pydantic, linting, and testing standards for implementation work.
- [PythonEngineeringStandards.md](./PythonEngineeringStandards.md) points to that shared standard and adds this project's addendum.
- [RalphPromptReferences.md](./RalphPromptReferences.md) defines the standard references and clauses to include in Ralph prompts.
