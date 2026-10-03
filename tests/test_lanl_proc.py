
from pathlib import Path

from graphsentinel.ingestion.lanl.proc import LANLProcessParser
from graphsentinel.schema import (
    EntityType,
    EventAction,
    TelemetryType,
)


def test_lanl_process_parser(tmp_path: Path):
    sample = tmp_path / "proc.txt"

    sample.write_text(
        "1,C1$@DOM1,C1,P16,Start\n"
        "1,C1001$@DOM1,C1001,P4,Start\n"
        "2,C1001$@DOM1,C1001,P4,End\n",
        encoding="utf-8",
    )

    parser = LANLProcessParser()
    events = list(parser.parse(sample))

    assert len(events) == 3

    event = events[0]

    assert event.telemetry_type == TelemetryType.ENDPOINT
    assert event.source.type == EntityType.HOST
    assert event.destination.type == EntityType.PROCESS
    assert event.source.id == "C1"
    assert event.destination.id == "P16"
    assert event.action == EventAction.EXECUTED
    assert event.attributes["user"] == "C1$@DOM1"
    assert event.attributes["process_event_type"] == "Start"
    assert event.attributes["dataset_time_seconds"] == 1

    assert events[2].attributes["process_event_type"] == "End"
