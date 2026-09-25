from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import EntityType


class Entity(BaseModel):
    """Canonical representation of a graph entity."""

    model_config = ConfigDict(extra="allow")

    id: str
    type: EntityType
    attributes: dict[str, Any] = Field(default_factory=dict)