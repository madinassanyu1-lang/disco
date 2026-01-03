import os
import json

from automation.error_audit import audit_error
from automation.config import CONFIG


def test_audit_error(tmp_path):
    logfile = tmp_path / "err.log"
    # temporarily override config path
    cfg_key = "ERROR_AUDIT_LOG"
    old = CONFIG.get(cfg_key)
    CONFIG[cfg_key] = str(logfile)
    try:
        entry = audit_error(step="t1", session_id="s1", page_url="http://example", message="oops", classification="Transient", ua="UA")
        assert entry["session_id"] == "s1"
        text = logfile.read_text()
        assert "oops" in text
    finally:
        CONFIG[cfg_key] = old
