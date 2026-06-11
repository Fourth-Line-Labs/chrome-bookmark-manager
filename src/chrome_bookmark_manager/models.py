from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field


class ChromeUrlNode(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: Literal["url"]
    id: str
    name: str
    url: str = Field(min_length=1)
    date_added: str | None = None


class ChromeFolderNode(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: Literal["folder"]
    id: str
    name: str
    children: list[ChromeUrlNode | Self]
    date_added: str | None = None
    date_modified: str | None = None


BookmarkNode = ChromeUrlNode | ChromeFolderNode


class ChromeRoots(BaseModel):
    model_config = ConfigDict(extra="ignore")

    bookmark_bar: ChromeFolderNode | None = None
    other: ChromeFolderNode | None = None
    synced: ChromeFolderNode | None = None


class ChromeBookmarksFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    roots: ChromeRoots
    version: int
