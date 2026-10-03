
from collections.abc import Iterator
from datetime import datetime, timezone
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


class LANLProcessParser:
    """Streaming parser for LANL process-activity records."""

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

        if len(fields) != 5:
            return None

        (
            timestamp,
            user,
            computer,
            process,
            process_event_type,
        ) = (field.strip() for field in fields)

        if not all(
            (timestamp, user, computer, process, process_event_type)
        ):
            return None

        timestamp_seconds = int(timestamp)

        # Temporary UTC-based representation.
        # Preserve the original dataset-relative timestamp separately.
        timestamp_value = datetime.fromtimestamp(
            timestamp_seconds,
            tz=timezone.utc,
        )

        return SecurityEvent(
            event_id=f"lanl-proc-{line_number}",
            timestamp=timestamp_value,
            telemetry_type=TelemetryType.ENDPOINT,
            source=EntityRef(
                type=EntityType.HOST,
                id=computer,
            ),
            destination=EntityRef(
                type=EntityType.PROCESS,
                id=process,
            ),
            action=EventAction.EXECUTED,
            result=EventResult.UNKNOWN,
            attributes={
                "dataset_time_seconds": timestamp_seconds,
                "user": user,
                "process_event_type": process_event_type,
            },
            source_metadata={
                "dataset": "LANL",
                "source_file_type": "process",
                "line_number": line_number,
            },
        )
