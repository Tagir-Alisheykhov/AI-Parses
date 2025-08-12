"""
    Файл-конфигурации переменных окружения.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class ShadowKeys:
    """Конфигурация чувствительных данных"""

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
