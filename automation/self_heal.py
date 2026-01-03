import json
import threading
from collections import Counter
from automation.config import CONFIG

_lock = threading.Lock()
RECENT_ERRORS_PATH = "recent_errors.json"
THRESHOLD = 3


def record_error_and_suggest(entry: dict):
    """Record the error (append to a small rolling JSON file) and if a pattern emerges write a suggestion."""
    with _lock:
        try:
            data = []
            try:
                with open(RECENT_ERRORS_PATH, "r") as f:
                    data = json.load(f)
            except Exception:
                data = []
            data.append(entry)
            # Keep size bounded
            data = data[-500:]
            with open(RECENT_ERRORS_PATH, "w") as f:
                json.dump(data, f)

            # Detect frequent messages
            msgs = [e.get("message") for e in data]
            counts = Counter(msgs)
            most_common, count = counts.most_common(1)[0] if counts else (None, 0)
            if most_common and count >= THRESHOLD:
                suggestion = f"Recurring issue: '{most_common}' seen {count} times; consider increasing wait time, verifying selectors, or toggling pacing."
                with open(CONFIG.get("UPGRADE_SUGGESTIONS", "upgrade_suggestions.txt"), "a") as f:
                    f.write(suggestion + "\n")
                return suggestion
        except Exception:
            # Don't let self-healing crash primary flow
            return None
    return None
