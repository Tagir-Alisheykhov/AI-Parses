import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def parse_page(session: aiohttp.ClientSession, url: str) -> dict | None:
    """Асинхронная функция для парсинга одной страницы"""
    try:
        async with session.get(url) as response:
            text = await response.text(encoding='utf-8')
            soup = BeautifulSoup(text, "html.parser")
            return {
                "url": url,
                "title": soup.find("title").text if soup.find("title") else "Без заголовка",
                "text": soup.get_text()[:2000]
            }
    except Exception as err:
        print(f"Ошибка при парсинге {url}: {err}")
        return None


async def main_parse(urls: list) -> list:
    """
    Главная асинхронная функция для парсинга.
    Для запуска: parsed_data = asyncio.run(main())
    """
    async with aiohttp.ClientSession() as session:
        tasks = [parse_page(session, url) for url in urls]
        # ожидание завершения всех задач
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]
