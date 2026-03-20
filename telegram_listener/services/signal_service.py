import requests

from telegram_listener.config.settings import get_settings

settings = get_settings()


def _base_url() -> str:
    return settings.DJANGO_API_URL.rstrip("/")


def _headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if settings.DJANGO_API_TOKEN:
        headers["Authorization"] = f"Token {settings.DJANGO_API_TOKEN}"
    return headers


def post_raw_message(data: dict) -> bool:
    url = f"{_base_url()}/raw-messages/"
    try:
        response = requests.post(url, json=data, headers=_headers(), timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error posting raw message: {e}")
        return False
