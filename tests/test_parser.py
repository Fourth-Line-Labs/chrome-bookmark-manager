import errno
import os
import shutil
import sys
from pathlib import Path
from typing import NoReturn

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
    # Without the check, the bounded read would still stop /dev/zero, but
    # with a misleading "too large" error instead of this one.
    with pytest.raises(BookmarkNotAFileError, match="not a regular file"):
        load_bookmarks_file(Path("/dev/zero"))


def test_file_over_size_limit_is_rejected(tmp_path: Path) -> None:
    bookmarks_file = tmp_path / "Bookmarks"
    shutil.copy(FIXTURES / "simple_bookmarks.json", bookmarks_file)
    limit = bookmarks_file.stat().st_size - 1

    with pytest.raises(BookmarkFileTooLargeError, match=f"larger than {limit} bytes"):
        load_bookmarks_file(bookmarks_file, max_bytes=limit)


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


@pytest.mark.skipif(
    sys.platform == "win32" or os.geteuid() == 0,
    reason="needs POSIX permissions and a non-root user",
)
def test_file_in_locked_directory_has_clear_error(tmp_path: Path) -> None:
    # exists() raises PermissionError here instead of returning False.
    locked = tmp_path / "locked"
    locked.mkdir()
    shutil.copy(FIXTURES / "simple_bookmarks.json", locked / "Bookmarks")
    locked.chmod(0)

    try:
        with pytest.raises(BookmarkReadError, match="Permission denied") as excinfo:
            load_bookmarks_file(locked / "Bookmarks")
    finally:
        locked.chmod(0o700)

    assert "[Errno" not in str(excinfo.value)


@pytest.mark.parametrize(
    ("error", "reason"),
    [
        (PermissionError(errno.EACCES, "Permission denied"), "Permission denied"),
        (OSError("no strerror available"), "no strerror available"),
    ],
)
def test_os_error_while_reading_has_clear_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    error: OSError,
    reason: str,
) -> None:
    """Covers the read-error branch on every platform, even as root."""
    bookmarks_file = tmp_path / "Bookmarks"
    shutil.copy(FIXTURES / "simple_bookmarks.json", bookmarks_file)

    def fail_open(*_args: object, **_kwargs: object) -> NoReturn:
        raise error

    monkeypatch.setattr(Path, "open", fail_open)

    with pytest.raises(BookmarkReadError, match=reason) as excinfo:
        load_bookmarks_file(bookmarks_file)

    # strerror is preferred over str(error), which would add "[Errno 13]".
    assert "[Errno" not in str(excinfo.value)
