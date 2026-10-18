from __future__ import annotations

from typing import TYPE_CHECKING

from chrome_bookmark_manager.errors.bookmark_parse_error import BookmarkParseError

if TYPE_CHECKING:
    from pathlib import Path


class BookmarkFileTooLargeError(BookmarkParseError):
    def __init__(self, path: Path, size: int, limit: int) -> None:
        super().__init__(
            f"Bookmark file is too large ({size} bytes; limit {limit}): {path}",
        )
