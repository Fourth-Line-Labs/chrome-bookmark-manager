from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pydantic import ValidationError

from chrome_bookmark_manager.errors import (
    BookmarkFileMissingError,
    BookmarkJsonError,
    BookmarkSchemaError,
)
from chrome_bookmark_manager.models import ChromeBookmarksFile

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def load_bookmarks_file(path: Path) -> ChromeBookmarksFile:
    if not path.exists():
        raise BookmarkFileMissingError(path)

    logger.info("Loading bookmarks from %s", path)
    content = path.read_text(encoding="utf-8")
    logger.debug("Read %d characters", len(content))
    try:
        bookmarks = ChromeBookmarksFile.model_validate_json(content)
    except ValidationError as error:
        if _is_json_error(error):
            raise BookmarkJsonError(path) from error
        raise BookmarkSchemaError(path, str(error)) from error

    logger.info("Parsed Chrome bookmarks file version %d", bookmarks.version)
    return bookmarks


def _is_json_error(error: ValidationError) -> bool:
    return any(item.get("type") == "json_invalid" for item in error.errors())
