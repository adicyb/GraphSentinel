from enum import Enum


class TelemetryType(str, Enum):
    """The major sources of security telemetry."""

    IDENTITY = "identity"
    NETWORK = "network"
    ENDPOINT = "endpoint"


class EntityType(str, Enum):
    """Types of entities represented in the GraphSentinel graph."""

    USER = "user"
    HOST = "host"
    PROCESS = "process"
    SERVICE = "service"


class EventAction(str, Enum):
    """Actions or relationships represented by security events."""

    AUTHENTICATED_TO = "AUTHENTICATED_TO"
    CONNECTED_TO = "CONNECTED_TO"
    EXECUTED = "EXECUTED"
    SPAWNED = "SPAWNED"


class EventResult(str, Enum):
    """Outcome of an event when an outcome is available."""

    SUCCESS = "success"
    FAILURE = "failure"
    UNKNOWN = "unknown"