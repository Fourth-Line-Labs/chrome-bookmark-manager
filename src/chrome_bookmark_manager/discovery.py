from __future__ import annotations

import logging
import os
import sys
from collections.abc import Callable, Mapping
from pathlib import Path, PurePath
from typing import Literal

from chrome_bookmark_manager.models import BookmarkCandidate

PlatformName = Literal["windows", "linux", "macos"]
PathExists = Callable[[PurePath], bool]

logger = logging.getLogger(__name__)


def current_platform() -> PlatformName:
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def discover_bookmark_files(
    *,
    platform: PlatformName | None = None,
    home: PurePath | None = None,
    env: Mapping[str, str] | None = None,
    path_exists: PathExists | None = None,
) -> list[BookmarkCandidate]:
    selected_platform = platform or current_platform()
    selected_home = home or Path.home()
    selected_env = os.environ if env is None else env
    exists = path_exists or _path_exists

    logger.debug(
        "Discovering bookmark files: platform=%s home=%s",
        selected_platform,
        selected_home,
    )
    candidates = candidate_bookmark_paths(
        platform=selected_platform,
        home=selected_home,
        env=selected_env,
    )
    found: list[BookmarkCandidate] = []
    for candidate in candidates:
        present = exists(candidate.path)
        logger.debug(
            "%s candidate %s (%s): %s",
            "Found" if present else "No",
            candidate.browser,
            candidate.profile,
            candidate.path,
        )
        if present:
            found.append(candidate)
    logger.info(
        "Found %d of %d candidate bookmark files",
        len(found),
        len(candidates),
    )
    return found


def candidate_bookmark_paths(
    *,
    platform: PlatformName,
    home: PurePath,
    env: Mapping[str, str],
) -> list[BookmarkCandidate]:
    if platform == "windows":
        local_app_data = env.get("LOCALAPPDATA")
        if not local_app_data:
            logger.warning(
                "LOCALAPPDATA is not set or is empty; "
                "cannot locate Windows bookmark files",
            )
            return []
        base = PurePath(local_app_data)
        return [
            BookmarkCandidate(
                "Google Chrome",
                "Default",
                base / "Google" / "Chrome" / "User Data" / "Default" / "Bookmarks",
            ),
            BookmarkCandidate(
                "Google Chrome",
                "Profile 1",
                base / "Google" / "Chrome" / "User Data" / "Profile 1" / "Bookmarks",
            ),
            BookmarkCandidate(
                "Chromium",
                "Default",
                base / "Chromium" / "User Data" / "Default" / "Bookmarks",
            ),
        ]

    if platform == "macos":
        app_support = home / "Library" / "Application Support"
        return [
            BookmarkCandidate(
                "Google Chrome",
                "Default",
                app_support / "Google" / "Chrome" / "Default" / "Bookmarks",
            ),
            BookmarkCandidate(
                "Google Chrome",
                "Profile 1",
                app_support / "Google" / "Chrome" / "Profile 1" / "Bookmarks",
            ),
            BookmarkCandidate(
                "Chromium",
                "Default",
                app_support / "Chromium" / "Default" / "Bookmarks",
            ),
        ]

    return [
        BookmarkCandidate(
            "Google Chrome",
            "Default",
            home / ".config" / "google-chrome" / "Default" / "Bookmarks",
        ),
        BookmarkCandidate(
            "Google Chrome",
            "Profile 1",
            home / ".config" / "google-chrome" / "Profile 1" / "Bookmarks",
        ),
        BookmarkCandidate(
            "Chromium",
            "Default",
            home / ".config" / "chromium" / "Default" / "Bookmarks",
        ),
    ]


def _path_exists(path: PurePath) -> bool:
    return Path(str(path)).exists()
