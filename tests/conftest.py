import logging
from collections.abc import Iterator
from pathlib import Path

import pytest

from chrome_bookmark_manager.logging_setup import LOG_DIR_ENV_VAR, LOGGER_NAME


@pytest.fixture(autouse=True)
def isolated_log_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Keep every test's log file out of the real user log directory."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv(LOG_DIR_ENV_VAR, str(log_dir))
    yield log_dir
    logger = logging.getLogger(LOGGER_NAME)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
