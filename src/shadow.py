"""
Файл-конфигурации переменных окружения.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class ShadowKeys:
    """Конфигурация чувствительных данных"""

    OPEN_ROUTER_AI_URL = os.getenv("OPEN_ROUTER_AI_URL")
    API_KEY = os.getenv("API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
