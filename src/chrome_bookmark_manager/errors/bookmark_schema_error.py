from __future__ import annotations

from typing import TYPE_CHECKING

from chrome_bookmark_manager.errors.bookmark_parse_error import BookmarkParseError

if TYPE_CHECKING:
    from pathlib import Path


class BookmarkSchemaError(BookmarkParseError):
    def __init__(self, path: Path, details: str) -> None:
        super().__init__(
            f"Bookmark file has an invalid Chrome schema: {path}: {details}",
        )
