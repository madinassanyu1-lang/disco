"""Simulate a full record check using masked PII and a dummy page that shows the OTP/fetchCode success screen.

This script is safe: it uses masked data stored in the repo and does not use or store raw PII.
"""
from automation.config import CONFIG
CONFIG["TEST_ENVIRONMENT"] = True

from run import Runner

# Monkeypatch in a dummy SessionManager that returns a success page
class DummyEl:
    def __init__(self, text, count=1):
        self._text = text
        self._count = count

    def count(self):
        return self._count

    def nth(self, i):
        return self

    def inner_text(self, timeout=None):
        return self._text

class DummyPage:
    def __init__(self, url, texts):
        self.url = url
        self._texts = texts

    def locator(self, sel):
        if "How can we send you a security code" in sel:
            return DummyEl(self._texts.get('otp',''), 1 if self._texts.get('otp') else 0)
        if "XXX-XXX-" in sel or "text=XXX-XXX-" in sel:
            return DummyEl(self._texts.get('phone',''), 1 if self._texts.get('phone') else 0)
        return DummyEl("", 0)

    def screenshot(self, path=None, full_page=False):
        with open(path, 'wb') as f:
            f.write(b'FAKEPNG')

    def content(self):
        return '<html>simulated success</html>'

class DummySessionManager:
    def __init__(self, page):
        self.page = page
    def start_session(self, prev_ua=None, proxy=None):
        return {"session_id": "sim-session-1", "ua": "Sim-UA", "page": self.page}
    def end_session(self, meta):
        return None

if __name__ == '__main__':
    # build a Runner using the masked sample
    page = DummyPage(url='https://portal.discover.com/web/account/recovery/challenge/otp/fetchCode', texts={'otp':'How can we send you a security code?','phone':'XXX-XXX-8146'})
    import run
    run.SessionManager = lambda *a, **k: DummySessionManager(page)

    r = Runner('sample_inputs/simulated_masked.csv')
    r.process_all()
    print('Summary:', r.meta)
    print('Success rows:', r.success_rows)
    print('Failed rows:', r.failed_rows)
