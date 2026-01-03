import time

COMMON_SPINNER_SELECTORS = [
    ".spinner",
    ".loading",
    "text=Please wait",
    "text=Hold tight",
    "text=Loading",
]


def wait_for_page_ready(page, timeout_ms: int = 15000, poll_ms: int = 300):
    """Poll DOM for absence of common loading indicators and presence of an enabled submit button.

    Returns (ready: bool, wait_seconds: float)
    """
    start = time.time()
    timeout = timeout_ms / 1000.0
    poll = poll_ms / 1000.0
    while True:
        try:
            spinner_present = any(page.locator(sel).count() > 0 for sel in COMMON_SPINNER_SELECTORS)
            submit_buttons = page.locator("button[type=submit]")
            submit_ready = submit_buttons.count() == 0 or any(submit_buttons.nth(i).is_enabled() for i in range(submit_buttons.count()))
            if not spinner_present and submit_ready:
                return True, time.time() - start
        except Exception:
            # On any DOM querying exception, continue polling until timeout
            pass
        if time.time() - start > timeout:
            return False, time.time() - start
        time.sleep(poll)
