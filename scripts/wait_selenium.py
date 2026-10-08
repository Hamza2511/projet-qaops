"""Wait for the Grid readiness flag, with a bounded startup deadline."""

import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit, urlunsplit


def status_url(remote_url):
    parts = urlsplit(remote_url)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError("SELENIUM_REMOTE_URL doit etre une URL HTTP(S)")
    path = parts.path.rstrip("/").removesuffix("/wd/hub")
    return urlunsplit((parts.scheme, parts.netloc, path + "/status", "", ""))


def wait_for_selenium(remote_url, timeout=60, interval=1):
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("SELENIUM_STARTUP_TIMEOUT doit etre un nombre positif fini")
    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("L'intervalle doit etre un nombre positif fini")
    url = status_url(remote_url)
    deadline = time.monotonic() + timeout
    attempts = 0
    last_error = "aucune reponse"
    while time.monotonic() < deadline:
        attempts += 1
        try:
            remaining = max(0.001, deadline - time.monotonic())
            with urllib.request.urlopen(url, timeout=min(2, remaining)) as response:
                payload = json.load(response)
            value = payload.get("value") if isinstance(payload, dict) else None
            if isinstance(value, dict) and value.get("ready") is True:
                print(f"Selenium disponible apres {attempts} tentative(s)", flush=True)
                return
            last_error = "le service ne renvoie pas value.ready=true"
        except (urllib.error.URLError, OSError, ValueError) as exc:
            # Do not echo URLs or exception bodies, which may contain credentials.
            last_error = type(exc).__name__
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(interval, remaining))
    raise TimeoutError(
        f"Selenium indisponible apres {timeout:g} s et {attempts} tentative(s) : {last_error}"
    )


def main():
    try:
        timeout = float(os.getenv("SELENIUM_STARTUP_TIMEOUT", "60"))
        wait_for_selenium(
            os.getenv("SELENIUM_REMOTE_URL", "http://selenium:4444"), timeout=timeout
        )
    except (ValueError, TimeoutError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
