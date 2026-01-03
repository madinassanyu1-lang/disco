import json
import time
import threading
from automation.config import CONFIG

_lock = threading.Lock()


def audit_error(step: str, session_id: str, page_url: str, message: str, classification: str, ua: str = None):
    entry = {
        "timestamp": time.time(),
        "session_id": session_id,
        "step": step,
        "page_url": page_url,
        "message": message,
        "classification": classification,
        "user_agent": ua,
    }
    line = json.dumps(entry)
    with _lock:
        with open(CONFIG.get("ERROR_AUDIT_LOG", "error_audit.log"), "a") as f:
            f.write(line + "\n")
    return entry
