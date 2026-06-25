import requests
from config import OPENAI_TOKEN


def generate_post(news_item):
    """Відправляє новину в OpenAI і отримує готовий пост для Telegram."""

    prompt = f"""
Ти — редактор Telegram-каналу про технології.
Зроби короткий (3-4 речення), цікавий пост на основі цієї новини.
Мова посту — українська.

Новина: {news_item['title']}
Джерело: {news_item['url']}
"""

    headers = {
        "Authorization": f"Bearer {OPENAI_TOKEN}",
        "Content-Type":  "application/json",
    }

    body = {
        "model": "gpt-4o-mini",   # дешевша модель, добре справляється
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()
        return text

    except Exception as e:
        print(f"[Помилка OpenAI]: {e}")
        # Якщо AI недоступний — повертаємо базовий пост
        return f" {news_item['title']}\n\n {news_item['url']}"