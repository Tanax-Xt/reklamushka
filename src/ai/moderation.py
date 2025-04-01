import json

import requests

from src.ai.config import api_key, api_url
from src.ai.services import add_message_to_response


def generate_message_to_moderation(text: str) -> list:
    messages = [
        {
            "role": "system",
            "text": "Ты — профессиональный корректор текстов с опытом проверки различных материалов для рекламного агенства. Проверь данный текст на наличие нецензурной брани, сексуального контекста, незаконной информации, упоминания наркотиков, насилия или запрещенных организаций. Выдай свой вердикт о корректности текста и краткое объяснение (1 предложение)",
        },
        {
            "role": "system",
            "text": 'Ответ вышли в формате json с полями block: bool и text: string, пример: {"block": true, "text": "Причина блокировки: ..."}. Никакого текста и лишнего форматирования кроме этого json.',
        },
        {
            "role": "user",
            "text": f"Текст для модерации: {text}",
        },
    ]

    return messages


def parse_moderation_data(data) -> dict | None:
    text = data["result"]["alternatives"][0]["message"]["text"]
    json_block_str = text.strip("`").strip()

    try:
        json_block = json.loads(json_block_str)
        block = json_block.get("block")
        reason_text = json_block.get("text")

        return {"block": block, "text": reason_text}
    except json.JSONDecodeError:
        try:
            status = data["result"]["alternatives"][0]["status"]
            if status != "ALTERNATIVE_STATUS_FINAL":
                return {"block": True, "text": "Причина блокировки: текст заблокирован фильтрами Яндекса"}
            return {"block": True, "text": "Причина блокировки: некорректный запрос, повторите попытку"}
        except:
            return None


def send_moderation_response(text: str):
    response = requests.post(
        api_url,
        json=add_message_to_response(generate_message_to_moderation(text)),
        headers={"Authorization": f"Api-Key {api_key}", "Content-Type": "application/json"},
    )

    if response.status_code == 200:
        data = response.json()
        return parse_moderation_data(data)

    return None
