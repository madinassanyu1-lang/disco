import time
import pytest

from automation.ui_detector import wait_for_ui_ready


class DummyLocator:
    def __init__(self, counts):
        self._counts = counts

    def count(self):
        return self._counts

    def nth(self, i):
        class B:
            def is_enabled(self):
                return True
        return B()


class DummyPage:
    def __init__(self, spinner_rounds=0):
        # spinner_rounds: number of polls the spinner exists
        self._spinner_rounds = spinner_rounds
        self._calls = 0

    def locator(self, sel):
        # simulate spinner present for first _spinner_rounds calls
        if "spinner" in sel or "Please wait" in sel or "Loading" in sel:
            if self._calls < self._spinner_rounds:
                return DummyLocator(1)
            else:
                return DummyLocator(0)
        # submit buttons
        return DummyLocator(0)

    def tick(self):
        self._calls += 1


def test_wait_for_ui_ready_no_spinner(monkeypatch):
    p = DummyPage(spinner_rounds=0)
    # monkeypatch time.sleep to advance page calls
    real_sleep = time.sleep

    def fake_sleep(s):
        p.tick()
        real_sleep(0)

    monkeypatch.setattr("time.sleep", fake_sleep)
    res = wait_for_ui_ready(p, timeout_ms=1000, poll_ms=100)
    assert res["ready"] is True


def test_wait_for_ui_ready_with_spinner(monkeypatch):
    p = DummyPage(spinner_rounds=3)
    real_sleep = time.sleep

    def fake_sleep(s):
        p.tick()
        real_sleep(0)

    monkeypatch.setattr("time.sleep", fake_sleep)
    res = wait_for_ui_ready(p, timeout_ms=2000, poll_ms=100)
    assert res["ready"] is True
    assert res["wait_seconds"] >= 0
