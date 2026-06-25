import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import NEWS_SOURCES, KEYWORDS

# Список вже оброблених новин (щоб не дублювати)
seen_urls = set()


def fetch_news(url):
    """Завантажує сторінку і витягує заголовки та посилання."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        news_items = []

        # Шукаємо всі посилання на сторінці
        for tag in soup.find_all("a", href=True):
            title = tag.get_text(strip=True)
            link  = tag["href"]

            # Беремо тільки посилання з текстом (не кнопки, не меню)
            if len(title) < 20:
                continue

            # Робимо посилання абсолютним якщо воно відносне
            if link.startswith("/"):
                from urllib.parse import urlparse
                base = urlparse(url)
                link = f"{base.scheme}://{base.netloc}{link}"

            if not link.startswith("http"):
                continue

            # Пропускаємо вже бачені
            if link in seen_urls:
                continue

            news_items.append({
                "title":        title,
                "url":          link,
                "summary":      title,   # для простоти беремо заголовок як summary
                "source":       url,
                "published_at": datetime.now().isoformat(),
            })

        return news_items

    except Exception as e:
        print(f"[Помилка парсингу] {url}: {e}")
        return []


def is_relevant(news_item):
    """Перевіряє чи містить новина ключові слова."""
    text = (news_item["title"] + " " + news_item["summary"]).lower()
    return any(kw.lower() in text for kw in KEYWORDS)


def get_fresh_news():
    """Збирає новини з усіх джерел і фільтрує їх."""
    all_news = []

    for source_url in NEWS_SOURCES:
        print(f"[Парсинг] {source_url}")
        items = fetch_news(source_url)

        for item in items:
            if is_relevant(item):
                seen_urls.add(item["url"])
                all_news.append(item)

    print(f"[Знайдено релевантних новин]: {len(all_news)}")
    return all_news