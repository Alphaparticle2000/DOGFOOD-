from typing import Any
import json
import urllib.request


def send_webhook(url: str, event: str, payload: dict[str, Any]) -> bool:
    body = json.dumps(
        {
            "event": event,
            "payload": payload,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return 200 <= response.status < 300
    except Exception:
        return False