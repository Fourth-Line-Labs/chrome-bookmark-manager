from pathlib import PurePath

from chrome_bookmark_manager.discovery import (
    BookmarkCandidate,
    candidate_bookmark_paths,
    discover_bookmark_files,
)


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
