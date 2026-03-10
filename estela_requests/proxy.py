import os
import logging

logger = logging.getLogger(__name__)

TUNNEL_HOST = "127.0.0.1"
TUNNEL_PORT = "8888"


def estela_proxy():
    if os.environ.get("ESTELA_PROXIES_ENABLED"):
        logger.debug("[proxy] Proxy active at %s:%s", TUNNEL_HOST, TUNNEL_PORT)
        return f"{TUNNEL_HOST}:{TUNNEL_PORT}"
    return None


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
            "chromium_arg": "--ignore-certificate-errors --ignore-ssl-errors",
        }
    return {}