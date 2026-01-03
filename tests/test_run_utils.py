import pytest
from automation.run_utils import classify_error, is_recoverable


def test_classify_transient():
    e = Exception("Network timeout while fetching")
    assert classify_error(e) == "Transient"
    assert is_recoverable("Transient")


def test_classify_captcha_hard_stop():
    e = Exception("Please complete the CAPTCHA to continue")
    assert classify_error(e) == "Hard stop"
    assert not is_recoverable("Hard stop")


def test_classify_validation():
    e = Exception("Validation failed: missing email")
    assert classify_error(e) == "Validation failure"
    assert not is_recoverable("Validation failure")


def test_classify_default_ui_inconsistency():
    e = Exception("DOMQueryError: missing node")
    assert classify_error(e) == "UI inconsistency"
    assert is_recoverable("UI inconsistency")
