import schedule
import time
from parser import get_fresh_news
from ai_generator import generate_post
from aibot.publisher import publish_post
from config import PARSE_INTERVAL_MINUTES


def pipeline():
    '''Головна послідовність: парсинг -> генерація -> публікація.'''
    print('\n=== Запуск pipeline ===')

    # 1. Збираємо новини
    news_list = get_fresh_news()

    if not news_list:
        print('[Pipeline] Нових релевантних новин не знайдено.')
        return

    # 2. Беремо першу найсвіжішу новину
    news = news_list[0]
    # 3. Генеруємо пост через AI
    post_text = generate_post(news)
    # 4. Публікуємо в Telegram
    publish_post(post_text)

# Запуск одразу при старті
pipeline()

# Потім — кожні N хвилин за розкладом
schedule.every(PARSE_INTERVAL_MINUTES).minutes.do(pipeline)
while True:
    schedule.run_pending()
    time.sleep(30)