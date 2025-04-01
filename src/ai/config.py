import os

api_key = os.getenv("YANDEX_GPT_API_KEY")
folder_id = os.getenv("FOLDER_ID")

api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
