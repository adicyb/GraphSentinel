
from collections.abc import Iterator
from dataclasses import dataclass
import gzip
from pathlib import Path


@dataclass(frozen=True)
class LANLRedTeamRecord:
    """A recorded Red Team activity entry from the LANL dataset."""

    timestamp_seconds: int
    user: str
    source_computer: str
    destination_computer: str
    line_number: int


class LANLRedTeamParser:
    """Streaming parser for LANL Red Team ground-truth records."""

    def parse(self, path: Path) -> Iterator[LANLRedTeamRecord]:
        opener = gzip.open if str(path).endswith(".gz") else open

        with opener(path, "rt", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    record = self._parse_line(line, line_number)
                except (ValueError, TypeError):
                    continue

                if record is not None:
                    yield record

    def _parse_line(
        self,
        line: str,
        line_number: int,
    ) -> LANLRedTeamRecord | None:
        fields = line.split(",")

        if len(fields) != 4:
            return None

        timestamp, user, source_computer, destination_computer = (
            field.strip() for field in fields
        )

        if not all(
            (timestamp, user, source_computer, destination_computer)
        ):
            return None

        return LANLRedTeamRecord(
            timestamp_seconds=int(timestamp),
            user=user,
            source_computer=source_computer,
            destination_computer=destination_computer,
            line_number=line_number,
        )
