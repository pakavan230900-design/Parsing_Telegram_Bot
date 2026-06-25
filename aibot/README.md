# AI-генератор постів для Telegram

Бот автоматично збирає новини з сайтів, генерує красиві пости через OpenAI та публікує їх у Telegram-канал за розкладом.

## Встановлення

```bash
pip install requests beautifulsoup4 openai python-telegram-bot schedule
```

## Налаштування

Відкрий `config.py` і заповни:

```python
OPENAI_API_KEY      = "твій ключ з platform.openai.com"
TELEGRAM_BOT_TOKEN  = "токен від @BotFather"
TELEGRAM_CHANNEL_ID = "@назва_каналу"
```

## Запуск

```bash
python main.py
```

## Структура проєкту

```
aibot/
├── main.py          # запуск і розклад
├── parser.py        # парсинг новин з сайтів
├── ai_generator.py  # генерація постів через OpenAI
├── publisher.py     # публікація в Telegram
├── config.py        # всі налаштування
└── README.md
```

## Як працює pipeline

```
Парсинг сайтів -> Фільтрація за ключовими словами -> AI-генерація поста -> Публікація в Telegram
```

## Функціональность


Збір новин (сайти) \
Фільтрація за ключовими словами. \
Виключення дублів. \
AI-генерація постів (OpenAI). \
Публікація в Telegram. \
Запуск за розкладом. \
Обробка помилок API. \