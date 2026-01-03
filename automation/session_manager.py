import uuid
import logging
import time
from typing import Optional

from automation.config import CONFIG
from automation.user_agents import rotate as rotate_ua
from automation.proxy import validate_proxy

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None

logger = logging.getLogger(__name__)


class SessionError(Exception):
    pass


class SessionManager:
    """Create fresh, incognito-equivalent sessions on each run.

    - Enforces TEST_ENVIRONMENT flag
    - Rotates UA
    - Validates proxy if provided
    - Returns a dict with session context info
    """

    def __init__(self):
        if not CONFIG.get("TEST_ENVIRONMENT"):
            raise SessionError("Forbidden: TEST_ENVIRONMENT is not enabled. Aborting.")
        if sync_playwright is None:
            logger.warning("Playwright not installed or import failed; session code will be inert until dependency is present.")

    def start_session(self, prev_ua: Optional[str] = None, proxy: Optional[dict] = None):
        if proxy and not validate_proxy(proxy):
            raise SessionError("Proxy validation failed; aborting session start.")
        session_id = str(uuid.uuid4())
        ua = rotate_ua(prev_ua)
        meta = {
            "session_id": session_id,
            "ua": ua,
            "proxy": proxy,
            "started_at": time.time(),
        }

        # Create Playwright context if available
        if sync_playwright:
            p = sync_playwright().start()
            browser = p.chromium.launch(headless=False)
            context_args = {"user_agent": ua, "viewport": {"width": 1366, "height": 768}}
            if proxy:
                context_args["proxy"] = {"server": proxy.get("server")}
            context = browser.new_context(**context_args)
            page = context.new_page()
            meta.update({"playwright": p, "browser": browser, "context": context, "page": page})
        else:
            # No-op placeholders so callers can still inspect meta during dry-runs
            meta.update({"playwright": None, "browser": None, "context": None, "page": None})

        logger.info("Started session %s with UA %s", session_id, ua)
        return meta

    def end_session(self, meta: dict):
        try:
            if meta.get("context"):
                meta["context"].close()
            if meta.get("browser"):
                meta["browser"].close()
            if meta.get("playwright"):
                meta["playwright"].stop()
        except Exception as e:
            logger.exception("Error during session cleanup: %s", e)
        finally:
            meta["ended_at"] = time.time()
