import requests

from app_logging import setup_logging

BASE_URL = "https://his.ppchat.vip"
RETRY_ATTEMPTS = 3
LOGGER = setup_logging()


def fetch_token_stats(token_key: str) -> dict:
    if not token_key:
        raise ValueError("token_key is not configured")

    last_error: Exception | None = None
    for attempt in range(RETRY_ATTEMPTS):
        try:
            resp = requests.get(
                f"{BASE_URL}/api/token-stats",
                params={"token_key": token_key},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json()
        except (requests.Timeout, requests.ConnectionError) as exc:
            last_error = exc
            LOGGER.warning(
                "token-stats request transient failure attempt=%s/%s error_type=%s",
                attempt + 1,
                RETRY_ATTEMPTS,
                type(exc).__name__,
            )
        except requests.HTTPError as exc:
            status_code = getattr(exc.response, "status_code", None)
            if status_code == 429 or (status_code is not None and status_code >= 500):
                last_error = exc
                LOGGER.warning(
                    "token-stats request http failure attempt=%s/%s status_code=%s",
                    attempt + 1,
                    RETRY_ATTEMPTS,
                    status_code,
                )
            else:
                raise

        if attempt == RETRY_ATTEMPTS - 1 and last_error is not None:
            LOGGER.error("token-stats request failed after retries")
            raise last_error

    raise RuntimeError("Failed to fetch token stats")
