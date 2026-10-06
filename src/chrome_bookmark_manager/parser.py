from __future__ import annotations

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


def load_bookmarks_file(path: Path) -> ChromeBookmarksFile:
    if not path.exists():
        raise BookmarkFileMissingError(path)

    content = path.read_text(encoding="utf-8")
    try:
        return ChromeBookmarksFile.model_validate_json(content)
    except ValidationError as error:
        if _is_json_error(error):
            raise BookmarkJsonError(path) from error
        raise BookmarkSchemaError(path, str(error)) from error


def _is_json_error(error: ValidationError) -> bool:
    return any(item.get("type") == "json_invalid" for item in error.errors())
