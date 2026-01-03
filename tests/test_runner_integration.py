import os
import json
from automation.config import CONFIG
from run import Runner


def test_runner_process_sample(tmp_path):
    CONFIG["TEST_ENVIRONMENT"] = True
    input_path = "sample_inputs/sample.csv"
    r = Runner(input_path)
    r.process_all()
    # summary file should exist
    assert os.path.exists(CONFIG.get("EXECUTION_SUMMARY"))
    with open(CONFIG.get("EXECUTION_SUMMARY")) as f:
        meta = json.load(f)
    assert "processed" in meta
