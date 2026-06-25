import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL_ID

# Зберігаємо вже опубліковані пости (щоб не дублювати)
published_posts = set()


def publish_post(text):
    """Відправляє пост у Telegram-канал через бота."""

    # Перевірка на дублікат
    if text in published_posts:
        print("[Пропуск] Цей пост вже публікувався.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id":    TELEGRAM_CHANNEL_ID,
        "text":       text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        published_posts.add(text)
        return True

    except Exception as e:
        print(f"[Помилка публікації]: {e}")
        return False