import logging
import os

logger = logging.getLogger(__name__)

TUNNEL_HOST = "127.0.0.1"
TUNNEL_PORT = "8888"


def estela_proxy():
    if os.environ.get("ESTELA_PROXIES_ENABLED"):
        logger.debug("[proxy] Proxy active at %s:%s", TUNNEL_HOST, TUNNEL_PORT)
        return f"{TUNNEL_HOST}:{TUNNEL_PORT}"
    return None


def estela_proxies():
    """
    Returns a requests-compatible proxies dict with upstream proxy credentials.
    For use with requests.Session (no mitmproxy tunnel needed).
    Returns an empty dict when proxy is disabled.

    Usage:
        from estela_requests.proxy import estela_proxies
        session = requests.Session()
        session.proxies = estela_proxies()
    """
    if not os.environ.get("ESTELA_PROXIES_ENABLED"):
        return {}
    user = os.environ.get("ESTELA_PROXY_USER", "")
    password = os.environ.get("ESTELA_PROXY_PASS", "")
    host = os.environ.get("ESTELA_PROXY_URL", "")
    port = os.environ.get("ESTELA_PROXY_PORT", "")
    if not all([user, password, host]):
        logger.warning("[proxy] Incomplete proxy variables.")
        return {}
    proxy_url = f"http://{user}:{password}@{host}:{port}"
    return {"http": proxy_url, "https": proxy_url}


def estela_driver_kwargs():
    """
    Returns the kwargs needed to configure a SeleniumBase Driver with proxy support.
    If proxy is disabled, returns an empty dict so the Driver works normally.

    Usage:
        from estela_requests.proxy import estela_driver_kwargs
        driver = Driver(browser="chrome", uc=True, **estela_driver_kwargs())
    """
    proxy = estela_proxy()
    if proxy:
        return {
            "proxy": proxy,
            "chromium_arg": "--ignore-certificate-errors",
        }
    return {}
