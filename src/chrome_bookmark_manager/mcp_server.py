"""Read-only MCP server exposing bookmark discovery and parsing over stdio.

Under the stdio transport, stdout carries the MCP protocol itself, so nothing
in this process may print to stdout. Logging goes to stderr and the log file.

This module deliberately omits ``from __future__ import annotations``: FastMCP
reads the tool functions' annotations at runtime to build their input and
output schemas, so the annotated types must be real runtime imports.

Start it through the ``chrome-bookmark-manager-mcp`` command. Running this file
with ``python -m`` would name the module ``__main__``, putting its logger
outside the package logger that ``configure_logging`` sets up.
"""

import argparse
import logging
import platform
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations

from chrome_bookmark_manager import __version__
from chrome_bookmark_manager.discovery import discover_bookmark_files
from chrome_bookmark_manager.errors import (
    BookmarkParseError,
    BookmarkPathExpansionError,
)
from chrome_bookmark_manager.logging_setup import configure_logging
from chrome_bookmark_manager.models import BookmarkCandidate, ChromeBookmarksFile
from chrome_bookmark_manager.parser import load_bookmarks_file
from chrome_bookmark_manager.renderer import render_markdown

logger = logging.getLogger(__name__)

SERVER_NAME = "chrome-bookmark-manager"
SERVER_INSTRUCTIONS = (
    "Read-only access to the user's Chrome and Chromium bookmarks. Call "
    "list_bookmark_files first to find bookmark files, then pass one of the "
    "returned paths to get_bookmark_tree or get_bookmarks_markdown. These tools "
    "never modify bookmarks."
)
READ_ONLY_TOOL = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)


def list_bookmark_files() -> list[BookmarkCandidate]:
    """List Chrome and Chromium bookmark files found on this computer.

    Checks the Bookmarks and AccountBookmarks files in common profiles. A file
    that is not listed can still be read by passing its path directly.
    """
    logger.info("Tool list_bookmark_files called")
    return discover_bookmark_files()


def get_bookmark_tree(path: str) -> ChromeBookmarksFile:
    """Return the folders and bookmarks in a Chrome bookmark file.

    The result keeps Chrome's structure: roots (bookmark bar, other, synced)
    containing nested folders and URL bookmarks.
    """
    logger.info("Tool get_bookmark_tree called for %s", path)
    return _load(path)


def get_bookmarks_markdown(path: str) -> str:
    """Return a Chrome bookmark file as a nested Markdown outline."""
    logger.info("Tool get_bookmarks_markdown called for %s", path)
    return render_markdown(_load(path))


def build_server() -> FastMCP:
    # FastMCP logs every request at INFO through the root logger; keep that off
    # stderr so the -v flags control what this server prints.
    server = FastMCP(
        SERVER_NAME,
        instructions=SERVER_INSTRUCTIONS,
        log_level="WARNING",
    )
    for tool in (list_bookmark_files, get_bookmark_tree, get_bookmarks_markdown):
        server.add_tool(tool, annotations=READ_ONLY_TOOL)
    return server


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    log_file = configure_logging(verbosity=args.verbose, log_file=args.log_file)
    logger.info("chrome-bookmark-manager MCP server %s starting", __version__)
    logger.debug(
        "Python %s on %s; arguments: %s",
        platform.python_version(),
        platform.platform(),
        sys.argv[1:] if argv is None else argv,
    )
    if log_file is not None:
        logger.info("Logging to %s", log_file)

    try:
        build_server().run("stdio")
    except Exception:
        logger.exception("MCP server stopped unexpectedly")
        raise
    logger.info("MCP server stopped")
    return 0


def _load(path: str) -> ChromeBookmarksFile:
    try:
        return load_bookmarks_file(_expand_home(path))
    except BookmarkParseError as error:
        logger.warning("%s", error)
        raise ToolError(str(error)) from error


def _expand_home(path: str) -> Path:
    try:
        return Path(path).expanduser()
    except RuntimeError as error:
        # Raised for an unknown ~user or when no home directory can be found.
        raise BookmarkPathExpansionError(path) from error


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chrome-bookmark-manager-mcp",
        description=(
            "Read-only MCP server for Chrome bookmarks. It speaks MCP over "
            "stdin/stdout, so start it from an MCP client, not by hand."
        ),
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
