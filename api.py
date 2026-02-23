import requests

BASE_URL = "https://his.ppchat.vip"


def fetch_token_stats(token_key: str) -> dict:
    if not token_key:
        raise ValueError("token_key is not configured")
    resp = requests.get(
        f"{BASE_URL}/api/token-stats",
        params={"token_key": token_key},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()
