"""Errors raised while loading Chrome bookmark files."""

from chrome_bookmark_manager.errors.bookmark_encoding_error import (
    BookmarkEncodingError,
)
from chrome_bookmark_manager.errors.bookmark_file_missing_error import (
    BookmarkFileMissingError,
)
from chrome_bookmark_manager.errors.bookmark_file_too_large_error import (
    BookmarkFileTooLargeError,
)
from chrome_bookmark_manager.errors.bookmark_json_error import BookmarkJsonError
from chrome_bookmark_manager.errors.bookmark_not_a_file_error import (
    BookmarkNotAFileError,
)
from chrome_bookmark_manager.errors.bookmark_parse_error import BookmarkParseError
from chrome_bookmark_manager.errors.bookmark_path_expansion_error import (
    BookmarkPathExpansionError,
)
from chrome_bookmark_manager.errors.bookmark_read_error import BookmarkReadError
from chrome_bookmark_manager.errors.bookmark_schema_error import BookmarkSchemaError

__all__ = [
    "BookmarkEncodingError",
    "BookmarkFileMissingError",
    "BookmarkFileTooLargeError",
    "BookmarkJsonError",
    "BookmarkNotAFileError",
    "BookmarkParseError",
    "BookmarkPathExpansionError",
    "BookmarkReadError",
    "BookmarkSchemaError",
]
