import os
import json
from automation.self_heal import record_error_and_suggest, RECENT_ERRORS_PATH
from automation.config import CONFIG

def test_self_heal_patterns(tmp_path):
    # point RECENT_ERRORS_PATH to tmp dir by monkeypatching module-level variable
    old = None
    try:
        # Clean leftover file if any
        if os.path.exists(RECENT_ERRORS_PATH):
            os.remove(RECENT_ERRORS_PATH)
        entry = {"message": "Timeout while waiting for spinner"}
        suggestion = None
        # write it 3 times to cross threshold
        for i in range(3):
            suggestion = record_error_and_suggest(entry)
        # After threshold, suggestion should be non-empty and upgrade_suggestions file should exist
        assert suggestion is not None
        assert os.path.exists(CONFIG.get("UPGRADE_SUGGESTIONS", "upgrade_suggestions.txt"))
    finally:
        # cleanup
        try:
            os.remove(RECENT_ERRORS_PATH)
        except Exception:
            pass
