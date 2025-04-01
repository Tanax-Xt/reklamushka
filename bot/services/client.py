import requests

from bot.config import api_url


def get_client_by_id(clientId):
    response = requests.get(api_url + f"/clients/{clientId}")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 404:
        return response.status_code, data["detail"]

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]


def send_client(client_id, login, age, location, gender):
    response = requests.post(
        api_url + "/clients/bulk",
        json=[{"client_id": client_id, "login": login, "age": age, "location": location, "gender": gender}],
    )

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data[0]

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]
