import random
import time

from typing import Optional


def human_type(locator, text: str, min_delay: float = 0.07, max_delay: float = 0.20):
    """Type character-by-character with variable delays and micro-pauses.

    `locator` is expected to have `type` or `fill` methods depending on the driver.
    This function prefers `type` method when available to mimic key-by-key entry.
    """
    if not text:
        return
    for ch in text:
        # Some drivers expose .type and some expect send_keys; adapt accordingly
        if hasattr(locator, "type"):
            locator.type(ch)
        elif hasattr(locator, "fill"):
            # Fallback: append and fill entire value (less realistic, but safe)
            current = locator.input_value() if hasattr(locator, "input_value") else ""
            locator.fill(current + ch)
        else:
            raise RuntimeError("Locator lacks typing methods")
        time.sleep(random.uniform(min_delay, max_delay))
    # Micro-pause after finishing a field
    time.sleep(random.uniform(0.15, 0.7))


def micro_pause(min_ms: int = 100, max_ms: int = 700):
    time.sleep(random.uniform(min_ms / 1000.0, max_ms / 1000.0))


def safe_click(page, selector: str, timeout: int = 10000):
    """Scroll into view, verify enabled state, and click with an occasional human pause."""
    el = page.locator(selector)
    el.scroll_into_view_if_needed()
    # Wait a short time for UI to stabilize
    micro_pause(80, 350)
    # Verify element readiness
    el.wait_for(state="visible", timeout=timeout)
    if not el.is_enabled():
        raise RuntimeError("Element not enabled for clicking")
    # Occasionally delay before clicking
    if random.random() < 0.2:
        micro_pause(150, 900)
    el.click()
