from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePath


@dataclass(frozen=True)
class BookmarkCandidate:
    browser: str
    profile: str
    path: PurePath
