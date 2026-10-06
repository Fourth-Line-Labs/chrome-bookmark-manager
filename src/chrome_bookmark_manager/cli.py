from __future__ import annotations

import argparse
import logging
import platform
import sys
from pathlib import Path
from typing import NoReturn

from chrome_bookmark_manager import __version__
from chrome_bookmark_manager.discovery import discover_bookmark_files
from chrome_bookmark_manager.errors import BookmarkParseError
from chrome_bookmark_manager.logging_setup import configure_logging
from chrome_bookmark_manager.parser import load_bookmarks_file
from chrome_bookmark_manager.renderer import render_markdown

logger = logging.getLogger(__name__)

UNEXPECTED_ERROR_EXIT_CODE = 1
PARSE_ERROR_EXIT_CODE = 2


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    log_file = configure_logging(verbosity=args.verbose, log_file=args.log_file)
    logger.info("chrome-bookmark-manager %s starting", __version__)
    logger.debug(
        "Python %s on %s; arguments: %s",
        platform.python_version(),
        platform.platform(),
        sys.argv[1:] if argv is None else argv,
    )
    if log_file is not None:
        logger.info("Logging to %s", log_file)

    try:
        exit_code = _run(parser, args)
    except Exception:
        logger.exception("Unexpected error")
        location = log_file if log_file is not None else "the console output above"
        sys.stderr.write(
            f"error: chrome-bookmark-manager failed unexpectedly. "
            f"Details: {location}\n",
        )
        return UNEXPECTED_ERROR_EXIT_CODE

    logger.info("Finished with exit code %d", exit_code)
    return exit_code


def _run(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
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
        logger.error("%s", error)  # noqa: TRY400 - expected input error, no traceback
        logger.debug("Parse failure detail", exc_info=error)
        return PARSE_ERROR_EXIT_CODE

    markdown = render_markdown(bookmarks)
    output = args.output
    if output is None:
        sys.stdout.write(markdown)
        return 0

    output.write_text(markdown, encoding="utf-8")
    logger.info("Wrote %d characters of Markdown to %s", len(markdown), output)
    sys.stdout.write(f"Wrote Markdown bookmark audit to {output}\n")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chrome-bookmark-manager",
        description="Read-only Chrome bookmark audit tool.",
        epilog=(
            "Every run writes a debug log. Set CHROME_BOOKMARK_MANAGER_LOG_DIR "
            "or pass --log-file to change where it goes; run with -v to print "
            "its location."
        ),
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
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Show more log output on stderr (-v for info, -vv for debug).",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Write the debug log here instead of the default location.",
    )
    return parser


def _entrypoint() -> NoReturn:
    raise SystemExit(main())


if __name__ == "__main__":
    _entrypoint()
