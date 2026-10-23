from __future__ import annotations

from typing import TYPE_CHECKING

from chrome_bookmark_manager.errors.bookmark_parse_error import BookmarkParseError

if TYPE_CHECKING:
    from pathlib import Path


class BookmarkReadError(BookmarkParseError):
    def __init__(self, path: Path, reason: str) -> None:
        super().__init__(f"Cannot read bookmark file {path}: {reason}")
