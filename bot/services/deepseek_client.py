import requests
from bot.core.config import settings

API_URL = settings.DEEPSEEK_URL
API_KEY = settings.DEEPSEEK_TOKEN


def ask_deepseek(message: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": message}],
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()

    return data["choices"][0]["message"]["content"]
