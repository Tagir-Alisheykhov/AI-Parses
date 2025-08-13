"""
    Точка входа, для запуска приложения.
"""

from src.handlers_bot import main

import asyncio
from datetime import datetime


if __name__ == "__main__":
    try:
        start_time = datetime.now()
        print("Запуск программы.. ")

        print(asyncio.run(main()))

        end_time = datetime.now()
        full_time = end_time - start_time
        print(f"Время выполнения: {full_time.total_seconds():.2f} секунд")
    except KeyboardInterrupt:
        print("Бот остановлен.")
