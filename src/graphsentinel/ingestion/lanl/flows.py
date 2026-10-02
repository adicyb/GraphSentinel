
from collections.abc import Iterator
import gzip
from pathlib import Path

from graphsentinel.schema import (
    EntityRef,
    EntityType,
    EventAction,
    EventResult,
    SecurityEvent,
    TelemetryType,
)


class LANLFlowParser:
    """Streaming parser for LANL network-flow records."""

    def parse(self, path: Path) -> Iterator[SecurityEvent]:
        opener = gzip.open if str(path).endswith(".gz") else open

        with opener(path, "rt", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    event = self._parse_line(line, line_number)
                except (ValueError, TypeError):
                    continue

                if event is not None:
                    yield event

    def _parse_line(
        self,
        line: str,
        line_number: int,
    ) -> SecurityEvent | None:
        fields = line.split(",")

        if len(fields) != 9:
            return None

        (
            timestamp,
            duration,
            source_computer,
            source_port,
            destination_computer,
            destination_port,
            protocol,
            packet_count,
            byte_count,
        ) = (field.strip() for field in fields)

        timestamp_seconds = int(timestamp)
        duration_value = float(duration)
        packet_count_value = int(packet_count)
        byte_count_value = int(byte_count)

        from datetime import datetime, timezone

        # Preserve LANL's dataset-relative timestamp in attributes.
        # The datetime is a UTC-based placeholder, not wall-clock event time.
        timestamp_value = datetime.fromtimestamp(
            timestamp_seconds,
            tz=timezone.utc,
        )

        return SecurityEvent(
            event_id=f"lanl-flow-{line_number}",
            timestamp=timestamp_value,
            telemetry_type=TelemetryType.NETWORK,
            source=EntityRef(
                type=EntityType.HOST,
                id=source_computer,
            ),
            destination=EntityRef(
                type=EntityType.HOST,
                id=destination_computer,
            ),
            action=EventAction.CONNECTED_TO,
            result=EventResult.UNKNOWN,
            attributes={
                "dataset_time_seconds": timestamp_seconds,
                "duration": duration_value,
                "source_port": source_port,
                "destination_port": destination_port,
                "protocol": protocol,
                "packet_count": packet_count_value,
                "byte_count": byte_count_value,
            },
            source_metadata={
                "dataset": "LANL",
                "source_file_type": "flows",
                "line_number": line_number,
            },
        )
