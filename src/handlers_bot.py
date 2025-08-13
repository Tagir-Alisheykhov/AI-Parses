"""
Обработчики сообщений телеграм бота.
"""

import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from src import utils
from src.connection_to_ai import ai_ask_answer
from src.parsing import main_parse
from src.shadow import ShadowKeys

shadow = ShadowKeys()
API_TOKEN = shadow.TELEGRAM_BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

parsed_data = list()


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Обрабатывает команду /start, отправляя приветствие."""
    await message.answer(
        "Привет! Задай вопрос о проектах EORA, и я "
        "постараюсь ответить на основе данных сайта."
    )


@dp.message()
async def handle_question(message: types.Message):
    """
    Основной обработчик сообщений.
    :param message: Сообщение от пользователя.
    """
    if not parsed_data:
        await message.answer("Бот еще не загрузил данные. Попробуйте позже.")
        return
    question = message.text
    await message.answer("ИИ думает..")
    context = utils.format_context_for_ai(data=parsed_data)
    try:
        raw_answer = await ai_ask_answer(
            ask_user=question, context=context, system_content=utils.system_content
        )
    except Exception as err:
        await message.answer(f"Ошибка ИИ: {err}")
        return
    linked_answer = utils.make_html_links(raw_answer, parsed_data)
    await message.answer(linked_answer, parse_mode="HTML")


async def on_startup():
    """Парсинг данных."""
    print("Парсинг сайта EORA...")
    global parsed_data
    parsed_data = await main_parse(urls=utils.urls)

    # Сохранение данных в файлы.
    os.makedirs("parsed_files", exist_ok=True)
    for i, item in enumerate(parsed_data):
        with open(f"parsed_files/page_{i+1}.txt", "w", encoding="UTF-8") as f:
            f.write(f"URL: {item['url']}\n\n")
            f.write(f"Заголовок: {item['title']}\n\n")
            f.write(item["text"])
    print(f"Спарсено {len(parsed_data)} страниц.")


async def main():
    """Запуск бота."""
    await on_startup()
    print("Бот запущен!")
    await dp.start_polling(bot)
