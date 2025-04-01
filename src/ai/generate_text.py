import json

import requests

from src.ai.config import api_key, api_url
from src.ai.services import add_message_to_response


def generate_message_to_generate_advertisement(product: str, advertiser_name: str, audience: str, target: str):
    messages = [
        {
            "role": "system",
            "text": "Ты — профессиональный маркетолог с опытом написания высококонверсионной рекламы. Для генерации рекламного объявления ты изучаешь потенциальную целевую аудиторию и оптимизируешь рекламный текст так, чтобы он обращался именно к этой целевой аудитории. Напиши рекламный текст для следующих продуктов/услуг учитывая специфику рекламодателя. Создай текст объявления с привлекающим внимание заголовком и убедительным призывом к действию, который побуждает пользователей к целевому действию. Учти, что текст будет размещаться в виде контекстной рекламы в интернете, люди не будут читать много текста. Длина текста до 500 символов",
        },
        {
            "role": "system",
            "text": 'Ответ вышли в формате json с полями title: string и text: string, пример: {"title": "Заголовок", "text": "Текст поста"}. Никакого текста и лишнего форматирования кроме этого json.',
        },
        {
            "role": "user",
            "text": f"Название рекламодателя: {advertiser_name}. Продукт/услуга: {product}. Целевое действие: {target}. Целевая аудитория: {audience}.",
        },
    ]

    return messages


def parse_generate_text_data(data) -> dict:
    text = data["result"]["alternatives"][0]["message"]["text"]
    json_block_str = text.strip("`").strip()

    try:
        json_block = json.loads(json_block_str)
        title = json_block.get("title")
        reason_text = json_block.get("text")

        return {"title": title, "text": reason_text}
    except json.JSONDecodeError:
        try:
            status = data["result"]["alternatives"][0]["status"]
            if status != "ALTERNATIVE_STATUS_FINAL":
                return {"title": "Недопустимая тема", "text": "Задана недопустимая тематика"}
            return {"title": "Сбой генерации", "text": "Не удалось сгенерировать текст"}
        except:
            return {"title": "Сбой генерации", "text": "Не удалось сгенерировать текст"}


def send_generate_text_response(
    product: str, advertiser_name: str, audience: str = "охвати как можно больше людей", target: str = "покупка"
) -> dict:
    response = requests.post(
        api_url,
        json=add_message_to_response(
            generate_message_to_generate_advertisement(product, advertiser_name, audience, target), 0.3
        ),
        headers={"Authorization": f"Api-Key {api_key}", "Content-Type": "application/json"},
    )

    if response.status_code == 200:
        data = response.json()
        return parse_generate_text_data(data)

    return {"title": "Сбой генерации", "text": "Не удалось сгенерировать текст"}
