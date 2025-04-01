import requests

from bot.config import api_url


def get_campaign_stat(campaign_id):
    response = requests.get(f"{api_url}/stats/campaigns/{campaign_id}")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def get_campaign_stat_daily(campaign_id):
    response = requests.get(f"{api_url}/stats/campaigns/{campaign_id}/daily")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def get_advertiser_stat(advertiser_id):
    response = requests.get(f"{api_url}/stats/advertisers/{advertiser_id}/campaigns")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def get_advertiser_stat_daily(advertiser_id):
    response = requests.get(f"{api_url}/stats/advertisers/{advertiser_id}/campaigns/daily")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]
