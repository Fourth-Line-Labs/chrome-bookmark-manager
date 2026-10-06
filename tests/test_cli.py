from pathlib import Path

import pytest

from chrome_bookmark_manager import cli
from chrome_bookmark_manager.cli import main
from chrome_bookmark_manager.logging_setup import LOG_FILE_NAME

FIXTURES = Path(__file__).parent / "fixtures" / "bookmarks"
PARSE_ERROR_EXIT_CODE = 2
UNEXPECTED_ERROR_EXIT_CODE = 1


def test_cli_writes_markdown_output(tmp_path: Path) -> None:
    output = tmp_path / "bookmarks.md"

    exit_code = main(
        [
            "--bookmarks-file",
            str(FIXTURES / "simple_bookmarks.json"),
            "--output",
            str(output),
        ],
    )

    assert exit_code == 0
    assert "- [Python](https://www.python.org/)" in output.read_text(encoding="utf-8")


def test_cli_reports_parse_errors(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing = tmp_path / "Bookmarks"

    exit_code = main(["--bookmarks-file", str(missing)])

    assert exit_code == PARSE_ERROR_EXIT_CODE
    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_cli_writes_run_log_to_default_location(isolated_log_dir: Path) -> None:
    bookmarks_file = FIXTURES / "simple_bookmarks.json"

    exit_code = main(["--bookmarks-file", str(bookmarks_file)])

    log = (isolated_log_dir / LOG_FILE_NAME).read_text(encoding="utf-8")
    assert exit_code == 0
    assert "chrome-bookmark-manager 0.1.0 starting" in log
    assert f"Loading bookmarks from {bookmarks_file}" in log
    assert "Finished with exit code 0" in log


def test_cli_log_file_option_overrides_location(tmp_path: Path) -> None:
    log_file = tmp_path / "custom" / "audit.log"

    main(
        [
            "--bookmarks-file",
            str(FIXTURES / "simple_bookmarks.json"),
            "--log-file",
            str(log_file),
        ]
    )

    assert "starting" in log_file.read_text(encoding="utf-8")


def test_cli_logs_never_contain_bookmark_content(isolated_log_dir: Path) -> None:
    main(["-vv", "--bookmarks-file", str(FIXTURES / "simple_bookmarks.json")])

    log = (isolated_log_dir / LOG_FILE_NAME).read_text(encoding="utf-8")
    assert "python.org" not in log


def test_cli_markdown_on_stdout_is_not_mixed_with_logs(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["-vv", "--bookmarks-file", str(FIXTURES / "simple_bookmarks.json")])

    captured = capsys.readouterr()
    assert captured.out.startswith("# Chrome Bookmarks")
    assert "DEBUG:" not in captured.out
    assert "DEBUG:" in captured.err


def test_cli_logs_parse_error_with_traceback(isolated_log_dir: Path) -> None:
    main(["--bookmarks-file", str(FIXTURES / "malformed.json")])

    log = (isolated_log_dir / LOG_FILE_NAME).read_text(encoding="utf-8")
    assert "ERROR" in log
    assert "not valid JSON" in log
    assert "Traceback" in log


def test_cli_unexpected_error_points_to_log_file(
    isolated_log_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def explode(_bookmarks: object) -> str:
        message = "renderer blew up"
        raise RuntimeError(message)

    monkeypatch.setattr(cli, "render_markdown", explode)

    exit_code = main(["--bookmarks-file", str(FIXTURES / "simple_bookmarks.json")])

    log_file = isolated_log_dir / LOG_FILE_NAME
    assert exit_code == UNEXPECTED_ERROR_EXIT_CODE
    assert str(log_file) in capsys.readouterr().err
    log = log_file.read_text(encoding="utf-8")
    assert "RuntimeError: renderer blew up" in log
    assert "Traceback" in log


def test_cli_schema_error_does_not_leak_bookmark_content(
    isolated_log_dir: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["--bookmarks-file", str(FIXTURES / "invalid_schema.json")])

    log = (isolated_log_dir / LOG_FILE_NAME).read_text(encoding="utf-8")
    err = capsys.readouterr().err
    assert "invalid Chrome schema" in log
    assert "Missing URL" not in log
    assert "Missing URL" not in err
