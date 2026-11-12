from pydantic import ConfigDict, Field

from src.schemas.base import BaseSchema


class AboutContent(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    about: str = Field(max_length=50_000)
