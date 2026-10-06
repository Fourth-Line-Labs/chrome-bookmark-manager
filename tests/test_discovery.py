from pathlib import PurePath

import pytest

from chrome_bookmark_manager.discovery import (
    candidate_bookmark_paths,
    discover_bookmark_files,
)
from chrome_bookmark_manager.models import BookmarkCandidate

WINDOWS_CANDIDATE_COUNT = 3


def test_linux_candidates_include_chrome_profiles_and_chromium() -> None:
    candidates = candidate_bookmark_paths(
        platform="linux",
        home=PurePath("/home/alex"),
        env={},
    )

    assert [candidate.path for candidate in candidates] == [
        PurePath("/home/alex/.config/google-chrome/Default/Bookmarks"),
        PurePath("/home/alex/.config/google-chrome/Profile 1/Bookmarks"),
        PurePath("/home/alex/.config/chromium/Default/Bookmarks"),
    ]


def test_macos_candidates_include_application_support_paths() -> None:
    candidates = candidate_bookmark_paths(
        platform="macos",
        home=PurePath("/Users/alex"),
        env={},
    )

    assert candidates[0].path == PurePath(
        "/Users/alex/Library/Application Support/Google/Chrome/Default/Bookmarks",
    )
    assert candidates[2].path == PurePath(
        "/Users/alex/Library/Application Support/Chromium/Default/Bookmarks",
    )


def test_windows_candidates_use_local_app_data() -> None:
    candidates = candidate_bookmark_paths(
        platform="windows",
        home=PurePath("C:/Users/alex"),
        env={"LOCALAPPDATA": "C:/Users/alex/AppData/Local"},
    )

    assert candidates[0].path == PurePath(
        "C:/Users/alex/AppData/Local/Google/Chrome/User Data/Default/Bookmarks",
    )
    assert candidates[1].path == PurePath(
        "C:/Users/alex/AppData/Local/Google/Chrome/User Data/Profile 1/Bookmarks",
    )
    assert candidates[2].path == PurePath(
        "C:/Users/alex/AppData/Local/Chromium/User Data/Default/Bookmarks",
    )


def test_discovery_returns_all_existing_candidates() -> None:
    existing = {
        PurePath("/home/alex/.config/google-chrome/Default/Bookmarks"),
        PurePath("/home/alex/.config/chromium/Default/Bookmarks"),
    }

    candidates = discover_bookmark_files(
        platform="linux",
        home=PurePath("/home/alex"),
        env={},
        path_exists=existing.__contains__,
    )

    assert candidates == [
        BookmarkCandidate(
            "Google Chrome",
            "Default",
            PurePath("/home/alex/.config/google-chrome/Default/Bookmarks"),
        ),
        BookmarkCandidate(
            "Chromium",
            "Default",
            PurePath("/home/alex/.config/chromium/Default/Bookmarks"),
        ),
    ]


WINDOWS_LOCAL_APP_DATA = "C:/Users/alex/AppData/Local"
WINDOWS_CHROME_DEFAULT = PurePath(
    "C:/Users/alex/AppData/Local/Google/Chrome/User Data/Default/Bookmarks",
)


def test_windows_discovery_reads_process_environment_when_env_omitted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", WINDOWS_LOCAL_APP_DATA)
    checked: list[PurePath] = []

    def path_exists(path: PurePath) -> bool:
        checked.append(path)
        return path == WINDOWS_CHROME_DEFAULT

    candidates = discover_bookmark_files(
        platform="windows",
        home=PurePath("C:/Users/alex"),
        path_exists=path_exists,
    )

    assert [candidate.path for candidate in candidates] == [WINDOWS_CHROME_DEFAULT]
    assert len(checked) == WINDOWS_CANDIDATE_COUNT


def test_windows_discovery_uses_injected_env_even_when_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", WINDOWS_LOCAL_APP_DATA)

    candidates = discover_bookmark_files(
        platform="windows",
        home=PurePath("C:/Users/alex"),
        env={},
        path_exists=lambda _path: True,
    )

    assert candidates == []


def test_windows_empty_local_app_data_yields_no_candidates() -> None:
    candidates = candidate_bookmark_paths(
        platform="windows",
        home=PurePath("C:/Users/alex"),
        env={"LOCALAPPDATA": ""},
    )

    assert candidates == []
