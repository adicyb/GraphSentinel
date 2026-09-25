from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import (
    EntityType,
    EventAction,
    EventResult,
    TelemetryType,
)


class EntityRef(BaseModel):
    """Reference to an entity participating in a security event."""

    model_config = ConfigDict(extra="allow")

    type: EntityType
    id: str


class SecurityEvent(BaseModel):
    """
    Canonical representation of a GraphSentinel security event.

    Dataset-specific telemetry will eventually be converted
    into this common format.
    """

    model_config = ConfigDict(extra="allow")

    event_id: str
    timestamp: datetime  # we need to know timestamp for temporal detection
    telemetry_type: TelemetryType # we need to know what telemetry are we getting identity,network,endpoint ?

    source: EntityRef  # source and destination gives us the relationship
    destination: EntityRef

    action: EventAction  #tells us what happened

    result: EventResult = EventResult.UNKNOWN

    attributes: dict[str, Any] = Field(default_factory=dict)

    source_metadata: dict[str, Any] = Field(default_factory=dict)