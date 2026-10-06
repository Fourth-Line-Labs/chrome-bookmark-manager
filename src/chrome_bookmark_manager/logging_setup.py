from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

from platformdirs import user_log_dir

if TYPE_CHECKING:
    from collections.abc import Mapping

APP_NAME = "chrome-bookmark-manager"
LOGGER_NAME = "chrome_bookmark_manager"
LOG_DIR_ENV_VAR = "CHROME_BOOKMARK_MANAGER_LOG_DIR"
LOG_FILE_NAME = "chrome-bookmark-manager.log"
MAX_LOG_BYTES = 1_000_000
LOG_BACKUP_COUNT = 3
DEBUG_VERBOSITY = 2

_FILE_FORMAT = "%(asctime)s %(levelname)-8s %(name)s [pid %(process)d] %(message)s"
_CONSOLE_FORMAT = "%(levelname)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def default_log_file(env: Mapping[str, str] | None = None) -> Path:
    selected_env = os.environ if env is None else env
    override = selected_env.get(LOG_DIR_ENV_VAR)
    if override:
        return Path(override) / LOG_FILE_NAME
    return Path(user_log_dir(APP_NAME, appauthor=False)) / LOG_FILE_NAME


def console_level(verbosity: int) -> int:
    if verbosity >= DEBUG_VERBOSITY:
        return logging.DEBUG
    if verbosity == 1:
        return logging.INFO
    return logging.WARNING


def configure_logging(*, verbosity: int, log_file: Path | None = None) -> Path | None:
    """Send package logs to stderr and a rotating file.

    Returns the log file in use, or None when it could not be opened. Calling
    this again replaces the handlers from the previous call.
    """
    logger = logging.getLogger(LOGGER_NAME)
    _remove_handlers(logger)
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(console_level(verbosity))
    console.setFormatter(logging.Formatter(_CONSOLE_FORMAT))
    logger.addHandler(console)

    target = default_log_file() if log_file is None else log_file
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            target,
            maxBytes=MAX_LOG_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
    except OSError as error:
        logger.warning("File logging disabled; cannot write %s: %s", target, error)
        return None

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_FILE_FORMAT, _DATE_FORMAT))
    logger.addHandler(file_handler)
    return target


def _remove_handlers(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
