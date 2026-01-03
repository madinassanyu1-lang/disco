import os
import json
import pytest
import requests

from automation.notifier import notify_incident


def test_notify_incident_no_alerts(monkeypatch, tmp_path):
    monkeypatch.setenv("ENABLE_ALERTS", "false")
    # should return False (alerts disabled)
    assert notify_incident("T", "B") is False


def test_notify_incident_slack(monkeypatch):
    # enable alerts and set webhook
    monkeypatch.setenv("ENABLE_ALERTS", "true")
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "http://example.com/slack")

    calls = {}

    def fake_post(url, json=None, headers=None, timeout=None):
        calls['url'] = url
        calls['json'] = json
        class R:
            def raise_for_status(self):
                return None
        return R()

    monkeypatch.setattr(requests, "post", fake_post)
    success = notify_incident("Title", "Body", severity="info")
    assert success is True
    assert calls['url'] == "http://example.com/slack"
    assert "Title" in calls['json']['text']


def test_notify_incident_pagerduty(monkeypatch):
    monkeypatch.setenv("ENABLE_ALERTS", "true")
    monkeypatch.setenv("PAGERDUTY_ROUTING_KEY", "abc123")
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "http://example.com/slack")

    posted = []

    def fake_post(url, json=None, headers=None, timeout=None):
        posted.append((url, json))
        class R:
            def raise_for_status(self):
                return None
        return R()

    monkeypatch.setattr(requests, "post", fake_post)
    # urgent true should trigger PagerDuty as well
    success = notify_incident("BigFailure", "Details here", severity="error", urgent=True)
    assert success is True
    # ensure both calls attempted (slack + pagerduty)
    urls = [p[0] for p in posted]
    assert any("slack" in u for u in urls)
    assert any("pagerduty" in u or "events.pagerduty.com" in u for u in urls)
