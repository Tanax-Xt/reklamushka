from src.ai.config import folder_id


def add_message_to_response(message: list, temperature: float = 0) -> dict:
    return {
        "modelUri": f"gpt://{folder_id}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": "2000",
            "reasoningOptions": {"mode": "DISABLED"},
        },
        "messages": message,
    }
