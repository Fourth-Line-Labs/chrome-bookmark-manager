from pathlib import Path

import pytest

from chrome_bookmark_manager.errors import (
    BookmarkFileMissingError,
    BookmarkJsonError,
    BookmarkSchemaError,
)
from chrome_bookmark_manager.parser import load_bookmarks_file

FIXTURES = Path(__file__).parent / "fixtures" / "bookmarks"


def test_loads_valid_bookmarks_file() -> None:
    bookmarks = load_bookmarks_file(FIXTURES / "simple_bookmarks.json")

    assert bookmarks.version == 1
    assert bookmarks.roots.bookmark_bar is not None
    assert bookmarks.roots.bookmark_bar.children[0].name == "Python"


def test_missing_file_has_clear_error(tmp_path: Path) -> None:
    with pytest.raises(BookmarkFileMissingError, match="does not exist"):
        load_bookmarks_file(tmp_path / "Bookmarks")


def test_malformed_json_has_clear_error() -> None:
    with pytest.raises(BookmarkJsonError, match="not valid JSON"):
        load_bookmarks_file(FIXTURES / "malformed.json")


def test_invalid_schema_has_clear_error() -> None:
    with pytest.raises(BookmarkSchemaError, match="invalid Chrome schema"):
        load_bookmarks_file(FIXTURES / "invalid_schema.json")
