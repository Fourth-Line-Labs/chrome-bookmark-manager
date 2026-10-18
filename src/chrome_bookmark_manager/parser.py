from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pydantic import ValidationError

from chrome_bookmark_manager.errors import (
    BookmarkEncodingError,
    BookmarkFileMissingError,
    BookmarkFileTooLargeError,
    BookmarkJsonError,
    BookmarkNotAFileError,
    BookmarkReadError,
    BookmarkSchemaError,
)
from chrome_bookmark_manager.models import ChromeBookmarksFile

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)

# Real Chrome bookmark files are a few MB at most. The cap stops a mistyped or
# hostile path from loading something huge into memory.
MAX_BOOKMARK_FILE_BYTES = 64 * 1024 * 1024


def load_bookmarks_file(
    path: Path,
    *,
    max_bytes: int = MAX_BOOKMARK_FILE_BYTES,
) -> ChromeBookmarksFile:
    if not path.exists():
        raise BookmarkFileMissingError(path)
    # Directories and special files such as /dev/zero pass exists(); reading
    # one fails or never finishes.
    if not path.is_file():
        raise BookmarkNotAFileError(path)

    logger.info("Loading bookmarks from %s", path)
    content = _read_text(path, max_bytes=max_bytes)
    logger.debug("Read %d characters", len(content))
    try:
        bookmarks = ChromeBookmarksFile.model_validate_json(content)
    except ValidationError as error:
        if _is_json_error(error):
            raise BookmarkJsonError(path) from error
        raise BookmarkSchemaError(path, str(error)) from error

    logger.info("Parsed Chrome bookmarks file version %d", bookmarks.version)
    return bookmarks


def _read_text(path: Path, *, max_bytes: int) -> str:
    try:
        size = path.stat().st_size
        if size > max_bytes:
            raise BookmarkFileTooLargeError(path, size, max_bytes)
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise BookmarkEncodingError(path) from error
    except OSError as error:
        raise BookmarkReadError(path, error.strerror or str(error)) from error


def _is_json_error(error: ValidationError) -> bool:
    return any(item.get("type") == "json_invalid" for item in error.errors())
