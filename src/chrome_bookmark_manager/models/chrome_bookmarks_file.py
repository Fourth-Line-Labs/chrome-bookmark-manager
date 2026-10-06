from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from chrome_bookmark_manager.models.chrome_roots import ChromeRoots


class ChromeBookmarksFile(BaseModel):
    model_config = ConfigDict(extra="ignore", hide_input_in_errors=True)

    roots: ChromeRoots
    version: int
