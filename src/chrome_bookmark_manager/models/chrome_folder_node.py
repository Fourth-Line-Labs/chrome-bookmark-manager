from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict

from chrome_bookmark_manager.models.chrome_url_node import ChromeUrlNode


class ChromeFolderNode(BaseModel):
    model_config = ConfigDict(extra="ignore", hide_input_in_errors=True)

    type: Literal["folder"]
    id: str
    name: str
    children: list[ChromeUrlNode | Self]
    date_added: str | None = None
    date_modified: str | None = None
