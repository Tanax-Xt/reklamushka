import requests

from bot.config import api_url


def get_advertiser_by_id(advertiserId):
    response = requests.get(api_url + f"/advertisers/{advertiserId}")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 404:
        return response.status_code, data["detail"]

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]


def send_ml_score(advertiser_id, client_id, ml_score):
    response = requests.post(
        api_url + "/ml-scores",
        json={"advertiser_id": advertiser_id, "client_id": client_id, "score": ml_score},
    )

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 404:
        return response.status_code, data["detail"]

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]


def send_advertiser(advertiser_id, name):
    response = requests.post(
        api_url + "/advertisers/bulk",
        json=[{"advertiser_id": advertiser_id, "name": name}],
    )

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data[0]

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]
