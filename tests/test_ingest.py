import pandas as pd

from ingest import fetch_and_save_csv


class FakeS3Client:
    def get_object(self, Bucket, Key):
        csv_data = """name,price
Property A,100
Property B,150
"""

        from io import BytesIO

        return {
            "Body": BytesIO(csv_data.encode("utf-8"))
        }


def test_ingestion_month(tmp_path):
    fake_s3 = FakeS3Client()

    output_file = tmp_path / "february.csv"

    fetch_and_save_csv(
        fake_s3,
        ["raw/february.csv"],
        str(output_file),
        "february"
    )

    result = pd.read_csv(output_file)

    assert result["ingestion_month"].iloc[0] == "february"


def test_ingestion_metadata_columns(tmp_path):
    fake_s3 = FakeS3Client()

    output_file = tmp_path / "january.csv"

    fetch_and_save_csv(
        fake_s3,
        ["raw/january.csv"],
        str(output_file),
        "january"
    )

    result = pd.read_csv(output_file)

    expected_columns = [
        "_snapshot_month",
        "_ingested_at",
        "_source_file",
        "ingestion_month"
    ]

    for column in expected_columns:
        assert column in result.columns

def test_source_file_metadata(tmp_path):
    fake_s3 = FakeS3Client()

    output_file = tmp_path / "june.csv"

    fetch_and_save_csv(
        fake_s3,
        ["raw/june.csv"],
        str(output_file),
        "june"
    )

    result = pd.read_csv(output_file)

    assert result["_source_file"].iloc[0] == "s3://ainowtaskaa/raw/june.csv"