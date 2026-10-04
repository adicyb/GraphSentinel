import argparse
from collections.abc import Iterable
from pathlib import Path

from numpy import record

from graphsentinel.ingestion.lanl import (
    LANLAuthParser,
    LANLFlowParser,
    LANLProcessParser,
    LANLRedTeamParser,
)


DATASET_PARSERS = {
    "auth": LANLAuthParser,
    "flows": LANLFlowParser,
    "proc": LANLProcessParser,
    "redteam": LANLRedTeamParser,
}


def validate_dataset(
    name: str,
    path: Path,
    parser,
    limit: int | None = None,
) -> dict[str, object]:
    records = parser.parse(path)

    count = 0
    first_timestamp = None
    last_timestamp = None

    for record in _limited(records, limit):
        count += 1

        if hasattr(record, "timestamp_seconds"):
            timestamp = record.timestamp_seconds
        else:
            timestamp = record.timestamp

        if first_timestamp is None:
            first_timestamp = timestamp

        last_timestamp = timestamp

    return {
        "dataset": name,
        "records": count,
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
    }


def _limited(records: Iterable, limit: int | None):
    for index, record in enumerate(records):
        if limit is not None and index >= limit:
            break

        yield record


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate GraphSentinel LANL parsers against raw datasets."
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory containing LANL .txt.gz files.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10000,
        help="Maximum records to inspect from each dataset.",
    )

    args = parser.parse_args()

    for name, parser_class in DATASET_PARSERS.items():
        path = args.data_dir / f"{name}.txt.gz"

        if not path.exists():
            print(f"{name.upper():8} MISSING  {path}")
            continue

        result = validate_dataset(
            name=name,
            path=path,
            parser=parser_class(),
            limit=args.limit,
        )

        print(
            f"{name.upper():8} "
            f"records={result['records']} "
            f"first={result['first_timestamp']} "
            f"last={result['last_timestamp']}"
        )


if __name__ == "__main__":
    main()