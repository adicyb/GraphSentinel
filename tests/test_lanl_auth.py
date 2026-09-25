from pathlib import Path

from graphsentinel.ingestion.lanl import LANLAuthParser
from graphsentinel.schema import (
    EntityType,
    EventAction,
    EventResult,
    TelemetryType,
)


def test_lanl_auth_parser(tmp_path: Path):
    sample = tmp_path / "auth.txt"

    sample.write_text(
        "100,user01@DOM,user02@DOM,COMP01,COMP02,Kerberos,Interactive,"
        "LogOn,Success\n",
        encoding="utf-8",
    )

    parser = LANLAuthParser()
    events = list(parser.parse(sample))

    assert len(events) == 1

    event = events[0]

    assert event.telemetry_type == TelemetryType.IDENTITY
    assert event.source.type == EntityType.USER
    assert event.destination.type == EntityType.HOST
    assert event.action == EventAction.AUTHENTICATED_TO
    assert event.result == EventResult.SUCCESS

    assert event.source.id == "user01@DOM"
    assert event.destination.id == "COMP02"
