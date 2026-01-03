import time
import logging
from typing import Optional
from automation.wait_utils import COMMON_SPINNER_SELECTORS

logger = logging.getLogger(__name__)


def wait_for_ui_ready(page, timeout_ms: int = 15000, poll_ms: int = 300):
    """Waits for spinners and common wait messages to clear.

    Returns a dict: {"ready": bool, "wait_seconds": float, "events": [list of observed events]}
    """
    start = time.time()
    timeout = timeout_ms / 1000.0
    poll = poll_ms / 1000.0
    # Track events observed during the most recent poll iteration
    observed = []

    while True:
        try:
            current_observed = []
            # Detect spinners/messages
            for sel in COMMON_SPINNER_SELECTORS:
                count = page.locator(sel).count()
                if count > 0:
                    current_observed.append(sel)
            # Detect disabled submit
            submit_buttons = page.locator("button[type=submit]")
            disabled_count = 0
            for i in range(submit_buttons.count()):
                if not submit_buttons.nth(i).is_enabled():
                    disabled_count += 1
            if disabled_count > 0:
                current_observed.append("disabled_submit")

            observed = current_observed

            if not observed:
                wait_seconds = time.time() - start
                logger.info("UI ready after %.2fs", wait_seconds)
                return {"ready": True, "wait_seconds": wait_seconds, "events": observed}
        except Exception:
            pass
        if time.time() - start > timeout:
            wait_seconds = time.time() - start
            logger.warning("UI not ready after %.2fs; observed: %s", wait_seconds, observed)
            return {"ready": False, "wait_seconds": wait_seconds, "events": observed}
        time.sleep(poll)
