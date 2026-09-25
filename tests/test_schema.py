from datetime import datetime, timezone

from graphsentinel.schema import (
    EntityRef,
    EntityType,
    EventAction,
    EventResult,
    SecurityEvent,
    TelemetryType,
)


def test_authentication_event():
    event = SecurityEvent(
        event_id="test-001",
        timestamp=datetime.now(timezone.utc),
        telemetry_type=TelemetryType.IDENTITY,
        source=EntityRef(
            type=EntityType.USER,
            id="user01",
        ),
        destination=EntityRef(
            type=EntityType.HOST,
            id="host01",
        ),
        action=EventAction.AUTHENTICATED_TO,
        result=EventResult.SUCCESS,
    )

    assert event.source.type == EntityType.USER
    assert event.destination.type == EntityType.HOST
    assert event.action == EventAction.AUTHENTICATED_TO
