import typing
from pathlib import PurePath

from chrome_bookmark_manager.models import BookmarkCandidate


def test_bookmark_candidate_type_hints_resolve_at_runtime() -> None:
    hints = typing.get_type_hints(BookmarkCandidate)

    assert hints == {"browser": str, "profile": str, "path": PurePath}
