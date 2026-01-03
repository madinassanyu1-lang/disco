import requests
import time

from automation.config import CONFIG


def validate_proxy(proxy: dict, timeout: float = 5.0) -> bool:
    """Validate proxy health by making a simple GET to a health URL.
    Proxy dict format example for requests/playwright: {"server": "http://ip:port", "username": ..., "password":...}
    Returns True if proxy appears healthy.
    """
    if not proxy:
        return True
    test_url = CONFIG.get("PROXY_HEALTH_TEST_URL")
    try:
        start = time.time()
        r = requests.get(test_url, proxies={"http": proxy.get("server"), "https": proxy.get("server")}, timeout=timeout)
        r.raise_for_status()
        return True
    except Exception:
        return False
