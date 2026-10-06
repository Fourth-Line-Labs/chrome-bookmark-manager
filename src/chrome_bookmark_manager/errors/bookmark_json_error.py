from __future__ import annotations

from typing import TYPE_CHECKING

from chrome_bookmark_manager.errors.bookmark_parse_error import BookmarkParseError

if TYPE_CHECKING:
    from pathlib import Path


class BookmarkJsonError(BookmarkParseError):
    def __init__(self, path: Path) -> None:
        super().__init__(f"Bookmark file is not valid JSON: {path}")
