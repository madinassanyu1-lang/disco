import os
import json
from automation.exporters import write_success_failed
from automation.config import CONFIG


def test_exporters_writes_files(tmp_path):
    success_rows = [{"input_id": "row-1", "session_id": "s1", "attempt": 1}]
    failed_rows = [{"input_id": "row-2", "reason": "validation"}]
    meta = {"processed": 2, "success": 1, "failed": 1}
    write_success_failed(success_rows, failed_rows, meta)
    # Check that outputs folder exists
    assert os.path.exists("outputs")
    # summary exists
    assert os.path.exists(CONFIG.get("EXECUTION_SUMMARY", "execution_summary.json"))
    with open(CONFIG.get("EXECUTION_SUMMARY", "execution_summary.json")) as f:
        m = json.load(f)
    assert m.get("processed") == 2
