import os
import csv
import tempfile
from automation.input_processor import load_input, validate_record


def test_load_csv_and_validate(tmp_path):
    path = tmp_path / "sample.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "name"])
        writer.writeheader()
        writer.writerow({"email": "a@example.com", "name": "A"})

    rows = load_input(str(path))
    assert len(rows) == 1
    assert rows[0]["input_id"].startswith("row-")
    assert validate_record(rows[0])


def test_load_txt_delimited(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("value1\nvalue2\n")
    rows = load_input(str(path))
    assert len(rows) == 2
    assert rows[0]["value"] == "value1"
