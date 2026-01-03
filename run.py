import time
import random
import json
import traceback
from automation.session_manager import SessionManager, SessionError
from automation.input_processor import load_input, validate_record
from automation.error_audit import audit_error
from automation.self_heal import record_error_and_suggest
from automation.exporters import write_success_failed
from automation.config import CONFIG
from automation.ui_detector import wait_for_ui_ready
from automation.human_interaction import micro_pause
from automation.run_utils import classify_error, is_recoverable


def exponential_backoff(attempt, base=0.5, max_s=30):
    jitter = random.uniform(0, 0.5 * base)
    delay = min(max_s, base * (2 ** attempt) + jitter)
    return delay


class Runner:
    def __init__(self, input_path: str):
        self.records = load_input(input_path)
        self.success_rows = []
        self.failed_rows = []
        self.meta = {"processed": 0, "success": 0, "failed": 0}
        self.session_mgr = SessionManager()

    def process_all(self):
        for rec in self.records:
            self.meta["processed"] += 1
            if not validate_record(rec):
                self.failed_rows.append({"input_id": rec.get("input_id"), "reason": "validation_failed"})
                continue
            attempt = 0
            while attempt <= CONFIG.get("MAX_RETRIES", 3):
                session = None
                try:
                    session = self.session_mgr.start_session()

                    # Wait for page ready and do a short human pause before interacting
                    page = session.get("page")
                    if page:
                        ready, wait_seconds = (True, 0)
                        try:
                            w = wait_for_ui_ready(page)
                            ready = w.get("ready", False)
                            wait_seconds = w.get("wait_seconds", 0)
                        except Exception:
                            # If UI checks throw, treat as not ready and allow retry
                            ready = False

                        if not ready:
                            raise RuntimeError("UI not ready after wait")

                        # Detect CAPTCHA-like states and abort
                        try:
                            if page.locator("text=captcha").count() > 0 or page.locator("text=are you human").count() > 0:
                                raise RuntimeError("CAPTCHA detected; aborting")
                        except Exception as e:
                            # If locator queries fail, proceed conservatively
                            if "CAPTCHA" in str(e) or "captcha" in str(e).lower():
                                raise RuntimeError("CAPTCHA detected; aborting")

                    # Placeholder: insert page interaction logic here (human-like typing, safe clicks, etc.)
                    # Simulate natural user pause before final submit
                    micro_pause()

                    # Simulate success
                    time.sleep(random.uniform(0.2, 0.5))
                    self.success_rows.append({"input_id": rec.get("input_id"), "session_id": session.get("session_id"), "attempt": attempt + 1})
                    self.meta["success"] += 1
                    break
                except SessionError as se:
                    # Abort session-level failures
                    audit_error(step="start_session", session_id="-", page_url="-", message=str(se), classification="Hard stop")
                    self.failed_rows.append({"input_id": rec.get("input_id"), "reason": "session_error", "error": str(se)})
                    self.meta["failed"] += 1
                    break
                except Exception as e:
                    classification = classify_error(e)
                    audit = audit_error(step="record_processing", session_id=(session.get("session_id") if session else "-"), page_url="-", message=str(e), classification=classification)
                    suggestion = record_error_and_suggest(audit)

                    if not is_recoverable(classification):
                        # Non-recoverable → fail fast for this record
                        self.failed_rows.append({"input_id": rec.get("input_id"), "reason": classification, "error": str(e)})
                        self.meta["failed"] += 1
                        break

                    if attempt == CONFIG.get("MAX_RETRIES", 3):
                        self.failed_rows.append({"input_id": rec.get("input_id"), "reason": "max_retries_exhausted", "error": str(e)})
                        self.meta["failed"] += 1
                        break
                    else:
                        delay = exponential_backoff(attempt, CONFIG.get("BACKOFF_BASE_SECONDS", 0.5), CONFIG.get("BACKOFF_MAX_SECONDS", 30))
                        time.sleep(delay)
                        attempt += 1
                finally:
                    if session:
                        try:
                            self.session_mgr.end_session(session)
                        except Exception:
                            pass
        # exports
        write_success_failed(self.success_rows, self.failed_rows, self.meta)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python run.py <input.(csv|xlsx|txt)>")
        sys.exit(2)
    runner = Runner(sys.argv[1])
    runner.process_all()
    print("Done. Summary:", runner.meta)
