from collections.abc import Iterator
from pathlib import Path
from typing import Protocol

from graphsentinel.schema import SecurityEvent


class EventParser(Protocol):
    """Interface implemented by telemetry-specific parsers."""

    def parse(self, path: Path) -> Iterator[SecurityEvent]:
        """Parse a telemetry source into canonical security events."""
        ...
