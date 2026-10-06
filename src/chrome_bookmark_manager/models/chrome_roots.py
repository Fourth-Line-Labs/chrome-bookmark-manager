from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from chrome_bookmark_manager.models.chrome_folder_node import ChromeFolderNode


class ChromeRoots(BaseModel):
    model_config = ConfigDict(extra="ignore")

    bookmark_bar: ChromeFolderNode | None = None
    other: ChromeFolderNode | None = None
    synced: ChromeFolderNode | None = None
