"""
    Подключение к ИИ.
"""

from openai import AsyncOpenAI

from src.shadow import ShadowKeys

shadow = ShadowKeys()
client = AsyncOpenAI(
    base_url=shadow.OPEN_ROUTER_AI_URL,
    api_key=shadow.API_KEY
)


async def ai_ask_answer(ask_user: str, context: str, system_content: str) -> str:
    """
    Обработка запроса пользователя и генерация ответа от AI.
    :param ask_user: Запрос пользователя.
    :param context: Контекст для анализа.
    :param system_content: Настройка поведения ai.
    :return: Ответ от ai
    """
    print("ИИ думает ... ")
    completion = await client.chat.completions.create(
        model="google/gemini-flash-1.5",
        messages=[
            {
                "role": "system",
                "content": f"{system_content}"
            },
            {
                "role": "user",
                "content": f"Контекст:\n{context}\n\nВопрос: {ask_user}"
            }
        ]
    )
    return completion.choices[0].message.content
