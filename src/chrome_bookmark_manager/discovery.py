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
# (browser, profile, profile directory)
ProfileDirectory = tuple[str, str, PurePath]

# Chrome keeps local bookmarks in "Bookmarks". Bookmarks saved to the user's
# Google Account without full Chrome Sync live beside them in
# "AccountBookmarks", in the same JSON format.
BOOKMARK_FILE_NAMES = ("Bookmarks", "AccountBookmarks")

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
    return [
        BookmarkCandidate(browser, profile, profile_dir / file_name)
        for browser, profile, profile_dir in _profile_directories(
            platform=platform,
            home=home,
            env=env,
        )
        for file_name in BOOKMARK_FILE_NAMES
    ]


def _profile_directories(
    *,
    platform: PlatformName,
    home: PurePath,
    env: Mapping[str, str],
) -> list[ProfileDirectory]:
    if platform == "windows":
        local_app_data = env.get("LOCALAPPDATA")
        if not local_app_data:
            logger.warning(
                "LOCALAPPDATA is not set or is empty; "
                "cannot locate Windows bookmark files",
            )
            return []
        base = PurePath(local_app_data)
        chrome = base / "Google" / "Chrome" / "User Data"
        return [
            ("Google Chrome", "Default", chrome / "Default"),
            ("Google Chrome", "Profile 1", chrome / "Profile 1"),
            ("Chromium", "Default", base / "Chromium" / "User Data" / "Default"),
        ]

    if platform == "macos":
        app_support = home / "Library" / "Application Support"
        chrome = app_support / "Google" / "Chrome"
        return [
            ("Google Chrome", "Default", chrome / "Default"),
            ("Google Chrome", "Profile 1", chrome / "Profile 1"),
            ("Chromium", "Default", app_support / "Chromium" / "Default"),
        ]

    config = home / ".config"
    return [
        ("Google Chrome", "Default", config / "google-chrome" / "Default"),
        ("Google Chrome", "Profile 1", config / "google-chrome" / "Profile 1"),
        ("Chromium", "Default", config / "chromium" / "Default"),
    ]


def _path_exists(path: PurePath) -> bool:
    return Path(str(path)).exists()
