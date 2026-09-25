from collections.abc import Iterator
from pathlib import Path
import gzip

from graphsentinel.schema import (
    EntityRef,
    EntityType,
    EventAction,
    EventResult,
    SecurityEvent,
    TelemetryType,
)


class LANLAuthParser:
    """
    Streaming parser for the LANL authentication event format.

    Expected LANL auth fields:

        time,
        source_user@domain,
        destination_user@domain,
        source_computer,
        destination_computer,
        authentication_type,
        logon_type,
        authentication_orientation,
        success/failure

    The parser intentionally preserves dataset-specific fields inside
    SecurityEvent.attributes rather than discarding them.
    """

    def parse(self, path: Path) -> Iterator[SecurityEvent]:
        opener = gzip.open if str(path).endswith(".gz") else open

        with opener(path, "rt", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    event = self._parse_line(line, line_number)
                except ValueError:
                    # Malformed records should not terminate a multi-GB
                    # ingestion job. They will be handled by validation
                    # and logging in a later ingestion layer.
                    continue

                if event is not None:
                    yield event

    def _parse_line(
        self,
        line: str,
        line_number: int,
    ) -> SecurityEvent | None:
        fields = line.split(",")

        if len(fields) < 9:
            return None

        (
            timestamp,
            source_user,
            destination_user,
            source_computer,
            destination_computer,
            authentication_type,
            logon_type,
            authentication_orientation,
            result,
            *extra,
        ) = fields

        timestamp_value = self._parse_timestamp(timestamp)

        event_result = self._parse_result(result)

        return SecurityEvent(
            event_id=f"lanl-auth-{line_number}",
            timestamp=timestamp_value,
            telemetry_type=TelemetryType.IDENTITY,
            source=EntityRef(
                type=EntityType.USER,
                id=source_user,
            ),
            destination=EntityRef(
                type=EntityType.HOST,
                id=destination_computer,
            ),
            action=EventAction.AUTHENTICATED_TO,
            result=event_result,
            attributes={
                "destination_user": destination_user,
                "source_computer": source_computer,
                "authentication_type": authentication_type,
                "logon_type": logon_type,
                "authentication_orientation": authentication_orientation,
                "extra_fields": extra,
            },
            source_metadata={
                "dataset": "LANL",
                "source_file_type": "auth",
                "line_number": line_number,
            },
        )

    @staticmethod
    def _parse_timestamp(value: str):
        from datetime import datetime, timezone

        seconds = int(value.strip())

        # LANL timestamps represent seconds from the beginning
        # of the dataset rather than Unix epoch timestamps.
        return datetime.fromtimestamp(seconds, tz=timezone.utc)

    @staticmethod
    def _parse_result(value: str) -> EventResult:
        normalized = value.strip().lower()

        if normalized in {"success", "1", "true"}:
            return EventResult.SUCCESS

        if normalized in {"failure", "fail", "0", "false"}:
            return EventResult.FAILURE

        return EventResult.UNKNOWN
