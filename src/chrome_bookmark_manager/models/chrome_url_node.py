from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ChromeUrlNode(BaseModel):
    model_config = ConfigDict(extra="ignore", hide_input_in_errors=True)

    type: Literal["url"]
    id: str
    name: str
    url: str = Field(min_length=1)
    date_added: str | None = None
