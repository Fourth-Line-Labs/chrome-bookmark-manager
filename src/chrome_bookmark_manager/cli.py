from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import NoReturn

from chrome_bookmark_manager.discovery import discover_bookmark_files
from chrome_bookmark_manager.errors import BookmarkParseError
from chrome_bookmark_manager.parser import load_bookmarks_file
from chrome_bookmark_manager.renderer import render_markdown


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list_discovered:
        candidates = discover_bookmark_files()
        if not candidates:
            sys.stdout.write("No Chrome or Chromium bookmark files found.\n")
            return 0
        for candidate in candidates:
            sys.stdout.write(
                f"{candidate.browser} ({candidate.profile}): {candidate.path}\n",
            )
        return 0

    bookmarks_file = args.bookmarks_file
    if bookmarks_file is None:
        parser.error("either --bookmarks-file or --list-discovered is required")

    try:
        bookmarks = load_bookmarks_file(bookmarks_file)
    except BookmarkParseError as error:
        sys.stderr.write(f"error: {error}\n")
        return 2

    markdown = render_markdown(bookmarks)
    output = args.output
    if output is None:
        sys.stdout.write(markdown)
        return 0

    output.write_text(markdown, encoding="utf-8")
    sys.stdout.write(f"Wrote Markdown bookmark audit to {output}\n")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chrome-bookmark-manager",
        description="Read-only Chrome bookmark audit tool.",
    )
    parser.add_argument(
        "--bookmarks-file",
        type=Path,
        help="Path to an explicit Chrome Bookmarks JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Markdown output path. Defaults to stdout.",
    )
    parser.add_argument(
        "--list-discovered",
        action="store_true",
        help="List discovered Chrome/Chromium bookmark files and exit.",
    )
    return parser


def _entrypoint() -> NoReturn:
    raise SystemExit(main())


if __name__ == "__main__":
    _entrypoint()
