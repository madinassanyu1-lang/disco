import csv
import json
from pathlib import Path
from typing import List, Dict


def load_input(path: str) -> List[Dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    if p.suffix.lower() in [".xlsx"]:
        try:
            import pandas as pd
        except Exception:
            raise RuntimeError("pandas required for .xlsx support")
        df = pd.read_excel(p)
        rows = df.to_dict(orient="records")
    elif p.suffix.lower() in [".csv"]:
        with open(p, newline="") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader]
    else:
        # Try to parse as delimited text (tab/pipe/comma)
        text = p.read_text().strip()
        if "\t" in text:
            delim = "\t"
        elif "|" in text:
            delim = "|"
        elif "," in text:
            delim = ","
        else:
            # single column
            rows = [{"value": line} for line in text.splitlines() if line.strip()]
            return rows
        reader = csv.DictReader(text.splitlines(), delimiter=delim)
        rows = [r for r in reader]

    # Normalize: ensure each row has an 'input_id'
    for idx, r in enumerate(rows):
        if "input_id" not in r:
            r["input_id"] = f"row-{idx+1}"
    return rows


def validate_record(rec: Dict) -> bool:
    # Example lightweight validation: check required fields are present
    # Customize as per target form fields
    # Skip records that are missing an email or username for instance
    if not rec:
        return False
    # All records must contain at least one non-empty value
    return any((v is not None and str(v).strip() for v in rec.values()))
