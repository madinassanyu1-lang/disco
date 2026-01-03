import types
import pytest

from automation.human_interaction import human_type


class DummyLocator:
    def __init__(self):
        self._value = ""

    def type(self, ch):
        self._value += ch

    def input_value(self):
        return self._value

    def fill(self, v):
        self._value = v


def test_human_type_types_characters(monkeypatch):
    # avoid actual sleep delays
    monkeypatch.setattr("time.sleep", lambda *a, **k: None)

    l = DummyLocator()
    human_type(l, "hello")
    assert l.input_value() == "hello"


def test_human_type_empty(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda *a, **k: None)
    l = DummyLocator()
    human_type(l, "")
    assert l.input_value() == ""
