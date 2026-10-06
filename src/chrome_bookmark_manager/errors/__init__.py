"""Errors raised while loading Chrome bookmark files."""

from chrome_bookmark_manager.errors.bookmark_file_missing_error import (
    BookmarkFileMissingError,
)
from chrome_bookmark_manager.errors.bookmark_json_error import BookmarkJsonError
from chrome_bookmark_manager.errors.bookmark_parse_error import BookmarkParseError
from chrome_bookmark_manager.errors.bookmark_schema_error import BookmarkSchemaError

__all__ = [
    "BookmarkFileMissingError",
    "BookmarkJsonError",
    "BookmarkParseError",
    "BookmarkSchemaError",
]
