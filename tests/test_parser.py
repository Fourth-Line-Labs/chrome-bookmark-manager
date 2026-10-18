import os
import shutil
import sys
from pathlib import Path

import pytest

from chrome_bookmark_manager.errors import (
    BookmarkEncodingError,
    BookmarkFileMissingError,
    BookmarkFileTooLargeError,
    BookmarkJsonError,
    BookmarkNotAFileError,
    BookmarkReadError,
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


def test_directory_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(BookmarkNotAFileError, match="not a regular file"):
        load_bookmarks_file(tmp_path)


@pytest.mark.skipif(not Path("/dev/zero").exists(), reason="needs /dev/zero")
def test_special_file_is_rejected_before_reading() -> None:
    # Reading /dev/zero never ends, so this would hang without the check.
    with pytest.raises(BookmarkNotAFileError, match="not a regular file"):
        load_bookmarks_file(Path("/dev/zero"))


def test_file_over_size_limit_is_rejected(tmp_path: Path) -> None:
    bookmarks_file = tmp_path / "Bookmarks"
    shutil.copy(FIXTURES / "simple_bookmarks.json", bookmarks_file)
    size = bookmarks_file.stat().st_size

    with pytest.raises(BookmarkFileTooLargeError, match=f"{size} bytes"):
        load_bookmarks_file(bookmarks_file, max_bytes=size - 1)


def test_file_at_size_limit_is_read(tmp_path: Path) -> None:
    bookmarks_file = tmp_path / "Bookmarks"
    shutil.copy(FIXTURES / "simple_bookmarks.json", bookmarks_file)

    bookmarks = load_bookmarks_file(
        bookmarks_file,
        max_bytes=bookmarks_file.stat().st_size,
    )

    assert bookmarks.version == 1


def test_non_utf8_file_has_clear_error(tmp_path: Path) -> None:
    bookmarks_file = tmp_path / "Bookmarks"
    bookmarks_file.write_bytes(b"\xff\xfe not utf-8")

    with pytest.raises(BookmarkEncodingError, match="not UTF-8 text"):
        load_bookmarks_file(bookmarks_file)


@pytest.mark.skipif(
    sys.platform == "win32" or os.geteuid() == 0,
    reason="needs POSIX permissions and a non-root user",
)
def test_unreadable_file_has_clear_error(tmp_path: Path) -> None:
    bookmarks_file = tmp_path / "Bookmarks"
    shutil.copy(FIXTURES / "simple_bookmarks.json", bookmarks_file)
    bookmarks_file.chmod(0)

    try:
        with pytest.raises(BookmarkReadError, match="Permission denied"):
            load_bookmarks_file(bookmarks_file)
    finally:
        bookmarks_file.chmod(0o600)
