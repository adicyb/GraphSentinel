
from pathlib import Path

from graphsentinel.ingestion.lanl.redteam import (
    LANLRedTeamParser,
    LANLRedTeamRecord,
)


def test_lanl_redteam_parser(tmp_path: Path):
    sample = tmp_path / "redteam.txt"

    sample.write_text(
        "150885,U620@DOM1,C17693,C1003\n"
        "151036,U748@DOM1,C17693,C305\n",
        encoding="utf-8",
    )

    parser = LANLRedTeamParser()
    records = list(parser.parse(sample))

    assert len(records) == 2

    record = records[0]

    assert isinstance(record, LANLRedTeamRecord)
    assert record.timestamp_seconds == 150885
    assert record.user == "U620@DOM1"
    assert record.source_computer == "C17693"
    assert record.destination_computer == "C1003"
    assert record.line_number == 1


def test_lanl_redteam_parser_skips_malformed_records(tmp_path: Path):
    sample = tmp_path / "redteam.txt"

    sample.write_text(
        "150885,U620@DOM1,C17693,C1003\n"
        "invalid_timestamp,U748@DOM1,C17693,C305\n"
        "151648,U748@DOM1,C17693\n"
        "\n",
        encoding="utf-8",
    )

    records = list(LANLRedTeamParser().parse(sample))

    assert len(records) == 1
    assert records[0].timestamp_seconds == 150885
