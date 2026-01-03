import os
import json
import time
import threading
import logging
from typing import Optional

import requests
from automation.config import CONFIG

logger = logging.getLogger(__name__)

# Config via env
ENABLE_ALERTS = os.environ.get("ENABLE_ALERTS", "false").lower() == "true"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
PAGERDUTY_ROUTING_KEY = os.environ.get("PAGERDUTY_ROUTING_KEY")
NOTIFIER_MAX_RETRIES = int(os.environ.get("NOTIFIER_MAX_RETRIES", 3))


class NotifierError(Exception):
    pass


def _post_with_retries(url: str, json_payload: dict, headers: dict = None):
    attempt = 0
    backoff_base = 0.5
    while attempt <= NOTIFIER_MAX_RETRIES:
        try:
            r = requests.post(url, json=json_payload, headers=headers, timeout=5)
            r.raise_for_status()
            return True
        except Exception as e:
            logger.warning("Notifier POST failed (attempt %s): %s", attempt + 1, e)
            attempt += 1
            time.sleep(min(10, backoff_base * (2 ** attempt)))
    return False


def _send_slack(message: str, channel: Optional[str] = None):
    if not SLACK_WEBHOOK_URL:
        raise NotifierError("SLACK_WEBHOOK_URL not configured")
    payload = {"text": message}
    if channel:
        payload["channel"] = channel
    return _post_with_retries(SLACK_WEBHOOK_URL, payload)


def _send_pagerduty(summary: str, severity: str = "error"):
    if not PAGERDUTY_ROUTING_KEY:
        raise NotifierError("PAGERDUTY_ROUTING_KEY not configured")
    payload = {
        "routing_key": PAGERDUTY_ROUTING_KEY,
        "event_action": "trigger",
        "payload": {
            "summary": summary,
            "severity": severity,
            "source": "automation-system",
        },
    }
    return _post_with_retries("https://events.pagerduty.com/v2/enqueue", payload)


def notify_incident(title: str, body: str, severity: str = "warning", urgent: bool = False):
    if not ENABLE_ALERTS:
        logger.info("Alerts disabled; skipping notify_incident")
        return False

    message = f"[{severity.upper()}] {title}: {body}"

    # send Slack (best-effort, non-blocking)
    def _send_all():
        try:
            try:
                _send_slack(message)
            except Exception as e:
                logger.warning("Slack notify failed: %s", e)
            if urgent:
                try:
                    _send_pagerduty(title, severity=("critical" if severity == "error" else severity))
                except Exception as e:
                    logger.warning("PagerDuty notify failed: %s", e)
        except Exception as e:
            logger.exception("Unhandled exception in notifier thread: %s", e)

    t = threading.Thread(target=_send_all, daemon=True)
    t.start()
    return True
