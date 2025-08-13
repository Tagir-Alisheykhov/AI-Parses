"""
Утилиты. Вспомогательный функционал приложения.
"""

import re

from aiogram.utils.markdown import hlink


def make_html_links(answer: str, parsed_data: list) -> str:
    """
    Преобразует [1], [2] и т.д. в HTML-ссылки с использованием aiogram.utils.markdown.hlink.
    Работает как декоратор для текста от ИИ.
    :param answer: Ответ от ИИ (строка с [1], [2] и т.д.)
    :param parsed_data: Спарсенные данные (список словарей с 'url')
    :return: Ответ с HTML-ссылками
    """

    def replace_match(match):
        # Получает номер из [1], [2] и т.д.
        num = int(match.group(1))
        if 1 <= num <= len(parsed_data):
            url = parsed_data[num - 1]["url"]
            # Возвращает HTML-ссылку: <a href="url">[1]</a>
            return hlink(f"[{num}]", url)
        else:
            # Если номер вне диапазона, оставляет как есть
            return match.group(0)

    # Ищет все метки и заменяет их на гиперссылки.
    result = re.sub(r"\[(\d+)\]", replace_match, answer)
    return result


def clean_json_block_in_context(text: str) -> str:
    """Удаляет JSON-блоки из текста."""
    pattern = r"\[\{.*?.*?}]"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return cleaned_text


def format_context_for_ai(data: list) -> str:
    """Форматирует контекст для ИИ (обычный текст с метками)."""
    formatted = []
    for i, item in enumerate(data):
        clean_text = clean_json_block_in_context(item["text"])
        formatted.append(f"[{i+1}] {item['title']}\n{clean_text}\nURL: {item['url']}")
    return "\n\n".join(formatted)


system_content = """
Ты — консультант компании EORA. Отвечай на русском языке.
Твоя задача — отвечать на вопросы, используя только информацию из предоставленного контекста.
Следуй этим правилам ОБЯЗАТЕЛЬНО:

1. ВСЕГДА ставь одну или несколько меток [1], [2], [3] и т.д. **только после** предложения, которое основано на информации из контекста.
2. КАЖДАЯ метка должна быть отдельной: [1], [2], [3]. НЕ используй списки вроде [1, 2, 3] или [1-5].
3. **НЕ ВЫВОДИ** отдельные строки вида: "[1] (https://...), [2] (https://...)". Это запрещено.
4. Метки должны идти НЕПОСРЕДСТВЕННО после информации, которую они подтверждают.
5. НЕ выводи строки вида "[1]: https://...".
6. Отвечай кратко, по делу и структурировано.
7. Если ты не нашел информацию в контексте, то предложи обратиться в нашу поддержку.

Пример:
Вопрос: Что делали для ритейлеров?
Ответ: Мы делали бота для HR [1]. Также мы создали систему поиска товаров по фото [2].

Пример НЕПРАВИЛЬНОГО ответа:
Вопрос: Как устроиться к вам на работу?
Ответ: В тексте указаны вакансии [1], [2], [3], ..., [33].  
(Такой ответ — неправильный, потому что просто перечисляет метки без контекста)

"""

urls = [
    "https://eora.ru/cases/promyshlennaya-bezopasnost",
    "https://eora.ru/cases/lamoda-systema-segmentacii-i-poiska-po-pohozhey-odezhde",
    "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/karas-golosovoy-assistent",
    "https://eora.ru/cases/assistenty-dlya-gorodov",
    "https://eora.ru/cases/avtomatizaciya-v-promyshlennosti/chemrar-raspoznovanie-molekul",
    "https://eora.ru/cases/zeptolab-skazki-pro-amnyama-dlya-sberbox",
    "https://eora.ru/cases/goosegaming-algoritm-dlya-ocenki-igrokov",
    "https://eora.ru/cases/dodo-pizza-robot-analitik-otzyvov",
    "https://eora.ru/cases/ifarm-nejroset-dlya-ferm",
    "https://eora.ru/cases/zhivibezstraha-navyk-dlya-proverki-rodinok",
    "https://eora.ru/cases/sportrecs-nejroset-operator-sportivnyh-translyacij",
    "https://eora.ru/cases/avon-chat-bot-dlya-zhenshchin",
    "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/navyk-dlya-proverki-loterejnyh-biletov",
    "https://eora.ru/cases/computer-vision/iss-analiz-foto-avtomobilej",
    "https://eora.ru/cases/purina-master-bot",
    "https://eora.ru/cases/skinclub-algoritm-dlya-ocenki-veroyatnostej",
    "https://eora.ru/cases/skolkovo-chat-bot-dlya-startapov-i-investorov",
    "https://eora.ru/cases/purina-podbor-korma-dlya-sobaki",
    "https://eora.ru/cases/purina-navyk-viktorina",
    "https://eora.ru/cases/dodo-pizza-pilot-po-avtomatizacii-kontakt-centra",
    "https://eora.ru/cases/dodo-pizza-avtomatizaciya-kontakt-centra",
    "https://eora.ru/cases/icl-bot-sufler-dlya-kontakt-centra",
    "https://eora.ru/cases/s7-navyk-dlya-podbora-aviabiletov",
    "https://eora.ru/cases/workeat-whatsapp-bot",
    "https://eora.ru/cases/absolyut-strahovanie-navyk-dlya-raschyota-strahovki",
    "https://eora.ru/cases/kazanexpress-poisk-tovarov-po-foto",
    "https://eora.ru/cases/kazanexpress-sistema-rekomendacij-na-sajte",
    "https://eora.ru/cases/intels-proverka-logotipa-na-plagiat",
    "https://eora.ru/cases/karcher-viktorina-s-voprosami-pro-uborku",
    "https://eora.ru/cases/chat-boty/purina-friskies-chat-bot-na-sajte",
    "https://eora.ru/cases/nejroset-segmentaciya-video",
    "https://eora.ru/cases/chat-boty/essa-nejroset-dlya-generacii-rolikov",
    "https://eora.ru/cases/qiwi-poisk-anomalij",
]
