
from pathlib import Path

from graphsentinel.ingestion.lanl.flows import LANLFlowParser
from graphsentinel.schema import (
    EntityType,
    EventAction,
    TelemetryType,
)


def test_lanl_flow_parser(tmp_path: Path):
    sample = tmp_path / "flows.txt"

    sample.write_text(
        "1,0,C1065,389,C3799,N10451,6,10,5323\n"
        "1,0,C1423,N1136,C1707,N1,6,5,847\n",
        encoding="utf-8",
    )

    parser = LANLFlowParser()
    events = list(parser.parse(sample))

    assert len(events) == 2

    event = events[0]

    assert event.telemetry_type == TelemetryType.NETWORK
    assert event.source.type == EntityType.HOST
    assert event.destination.type == EntityType.HOST
    assert event.source.id == "C1065"
    assert event.destination.id == "C3799"
    assert event.action == EventAction.CONNECTED_TO
    assert event.attributes["source_port"] == "389"
    assert event.attributes["destination_port"] == "N10451"
    assert event.attributes["packet_count"] == 10
    assert event.attributes["byte_count"] == 5323
    assert event.attributes["dataset_time_seconds"] == 1
