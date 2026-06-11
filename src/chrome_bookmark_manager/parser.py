from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import ValidationError

from chrome_bookmark_manager.models import ChromeBookmarksFile

if TYPE_CHECKING:
    from pathlib import Path


class BookmarkParseError(Exception):
    """Base class for bookmark input errors."""


class BookmarkFileMissingError(BookmarkParseError):
    def __init__(self, path: Path) -> None:
        super().__init__(f"Bookmark file does not exist: {path}")


class BookmarkJsonError(BookmarkParseError):
    def __init__(self, path: Path) -> None:
        super().__init__(f"Bookmark file is not valid JSON: {path}")


class BookmarkSchemaError(BookmarkParseError):
    def __init__(self, path: Path, details: str) -> None:
        super().__init__(
            f"Bookmark file has an invalid Chrome schema: {path}: {details}",
        )


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
