import io
import logging
from pathlib import Path

import pytest
from platformdirs import user_log_dir

from chrome_bookmark_manager.logging_setup import (
    APP_NAME,
    LOG_DIR_ENV_VAR,
    LOG_FILE_NAME,
    LOGGER_NAME,
    configure_logging,
    console_level,
    default_log_file,
)


def test_default_log_file_uses_env_override() -> None:
    log_file = default_log_file({LOG_DIR_ENV_VAR: "/srv/cbm-logs"})

    assert log_file == Path("/srv/cbm-logs") / LOG_FILE_NAME


def test_default_log_file_falls_back_to_platform_log_dir() -> None:
    log_file = default_log_file({})

    assert log_file == Path(user_log_dir(APP_NAME, appauthor=False)) / LOG_FILE_NAME


def test_default_log_file_reads_process_environment(isolated_log_dir: Path) -> None:
    assert default_log_file() == isolated_log_dir / LOG_FILE_NAME


@pytest.mark.parametrize(
    ("verbosity", "expected"),
    [(0, logging.WARNING), (1, logging.INFO), (2, logging.DEBUG), (5, logging.DEBUG)],
)
def test_console_level_maps_verbosity(verbosity: int, expected: int) -> None:
    assert console_level(verbosity) == expected


def test_file_receives_debug_records_regardless_of_verbosity(tmp_path: Path) -> None:
    log_file = tmp_path / "run.log"

    used = configure_logging(verbosity=0, log_file=log_file)
    logging.getLogger(f"{LOGGER_NAME}.test").debug("detail for the file")

    assert used == log_file
    assert "detail for the file" in log_file.read_text(encoding="utf-8")


def test_default_location_is_created(isolated_log_dir: Path) -> None:
    used = configure_logging(verbosity=0)

    assert used == isolated_log_dir / LOG_FILE_NAME
    assert isolated_log_dir.is_dir()


def test_reconfiguring_does_not_duplicate_output(tmp_path: Path) -> None:
    log_file = tmp_path / "run.log"

    configure_logging(verbosity=0, log_file=log_file)
    configure_logging(verbosity=0, log_file=log_file)
    logging.getLogger(LOGGER_NAME).info("only once")

    assert log_file.read_text(encoding="utf-8").count("only once") == 1


def test_console_is_quiet_by_default(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(verbosity=0, log_file=tmp_path / "run.log")
    logger = logging.getLogger(LOGGER_NAME)
    logger.info("routine progress")
    logger.warning("something odd")

    captured = capsys.readouterr()
    assert "routine progress" not in captured.err
    assert "WARNING: something odd" in captured.err
    assert captured.out == ""


def test_verbose_console_shows_info_on_stderr(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(verbosity=1, log_file=tmp_path / "run.log")
    logging.getLogger(LOGGER_NAME).info("routine progress")

    captured = capsys.readouterr()
    assert "INFO: routine progress" in captured.err
    assert captured.out == ""


def test_unwritable_log_location_disables_file_logging(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("", encoding="utf-8")

    used = configure_logging(verbosity=0, log_file=blocker / "run.log")

    assert used is None
    assert "File logging disabled" in capsys.readouterr().err


def test_configured_logs_do_not_propagate_to_root_handlers(tmp_path: Path) -> None:
    root_stream = io.StringIO()
    root_handler = logging.StreamHandler(root_stream)
    root = logging.getLogger()
    root.addHandler(root_handler)
    try:
        configure_logging(verbosity=0, log_file=tmp_path / "run.log")
        logging.getLogger(f"{LOGGER_NAME}.test").warning("emitted once")
    finally:
        root.removeHandler(root_handler)

    assert root_stream.getvalue() == ""
    assert "emitted once" in (tmp_path / "run.log").read_text(encoding="utf-8")
