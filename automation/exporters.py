import json
from pathlib import Path
from automation.config import CONFIG

try:
    import pandas as pd
except Exception:
    pd = None


def write_success_failed(success_rows, failed_rows, meta):
    # Accept list-of-dicts
    Path("outputs").mkdir(exist_ok=True)
    if pd:
        pd.DataFrame(success_rows).to_excel("outputs/success.xlsx", index=False)
        pd.DataFrame(success_rows).to_csv("outputs/success.csv", index=False)
        pd.DataFrame(success_rows).to_json("outputs/success.txt", orient="records")

        pd.DataFrame(failed_rows).to_excel("outputs/failed.xlsx", index=False)
        pd.DataFrame(failed_rows).to_csv("outputs/failed.csv", index=False)
        pd.DataFrame(failed_rows).to_json("outputs/failed.txt", orient="records")
    else:
        # Minimal textual fallbacks
        with open("outputs/success.txt", "w") as f:
            f.write(json.dumps(success_rows, indent=2))
        with open("outputs/failed.txt", "w") as f:
            f.write(json.dumps(failed_rows, indent=2))

    with open(CONFIG.get("EXECUTION_SUMMARY", "execution_summary.json"), "w") as f:
        json.dump(meta, f, indent=2)
