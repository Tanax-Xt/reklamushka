import requests

from bot.config import api_url


def click_ad(ad_id, client_id):
    response = requests.post(
        f"{api_url}/ads/{ad_id}/click",
        json={"client_id": client_id},
    )

    if response.status_code == 204:
        return response.status_code, None

    data = response.json()

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def get_ad(client_id):
    response = requests.get(f"{api_url}/ads?client_id={client_id}")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def get_ad_image(advertiser_id, campaign_id):
    response = requests.get(f"{api_url}/advertisers/{advertiser_id}/campaigns/{campaign_id}/image")

    if response.status_code == 200:
        return response.status_code, response.content

    return response.status_code, None
