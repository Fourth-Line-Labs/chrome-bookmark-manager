from pathlib import Path

import pytest

from chrome_bookmark_manager.cli import main

FIXTURES = Path(__file__).parent / "fixtures" / "bookmarks"
PARSE_ERROR_EXIT_CODE = 2


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
