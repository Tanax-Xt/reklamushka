import requests

from bot.config import api_url


def get_current_date() -> int | None:
    response = requests.get(api_url + "/time")

    if response.status_code == 200:
        data = response.json()
        return data["current_date"]

    return None


def send_new_date(date):
    response = requests.post(api_url + "/time/advance", json={"current_date": date})
    data = response.json()

    if response.status_code == 200:
        return response.status_code, data["current_date"]

    if response.status_code == 409:
        return response.status_code, data["detail"]

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]
