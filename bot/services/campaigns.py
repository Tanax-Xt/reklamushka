import tempfile

import requests

from bot.config import api_url


def post_moderation_mode(mode: bool):
    response = requests.post(api_url + "/ai/moderation-campaigns", json={"current_state": mode})

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def get_generate_ai_text(advertiser_name, product):
    response = requests.post(
        api_url + "/ai/generate-text",
        json={"advertiser_name": advertiser_name, "product": product},
    )

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def post_campaign(
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
        campaign_start_date,
        campaign_end_date,
        target_gender,
        target_age_from,
        target_age_to,
        target_location,
):
    response = requests.post(
        f"{api_url}/advertisers/{advertiser_id}/campaigns",
        json={
            "impressions_limit": impressions_limit,
            "clicks_limit": clicks_limit,
            "cost_per_impression": cost_per_impression,
            "cost_per_click": cost_per_click,
            "ad_title": campaign_name,
            "ad_text": campaign_text,
            "start_date": campaign_start_date,
            "end_date": campaign_end_date,
            "targeting": {
                "gender": target_gender,
                "age_from": target_age_from,
                "age_to": target_age_to,
                "location": target_location,
            },
        },
    )

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def get_campaign(advertiser_id, campaign_id):
    response = requests.get(f"{api_url}/advertisers/{advertiser_id}/campaigns/{campaign_id}")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def put_campaign(campaign_id, advertiser_id, target_gender, target_age_from, target_age_to, target_location):
    status_code, response = get_campaign(advertiser_id, campaign_id)
    if status_code == 200:
        response["targeting"]["gender"] = target_gender
        response["targeting"]["age_from"] = target_age_from
        response["targeting"]["age_to"] = target_age_to
        response["targeting"]["location"] = target_location

        response = requests.put(
            f"{api_url}/advertisers/{advertiser_id}/campaigns/{campaign_id}",
            json=response,
        )

        data = response.json()

        if response.status_code == 200:
            return response.status_code, data

        if response.status_code == 422:
            return response.status_code, data["detail"][0]["msg"]

        return response.status_code, data["detail"]

    return status_code, response


def get_campaigns(advertiser_id):
    response = requests.get(f"{api_url}/advertisers/{advertiser_id}/campaigns")

    data = response.json()

    if response.status_code == 200:
        return response.status_code, data

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]


def patch_image_campaign(campaign_id, advertiser_id, downloaded_file):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".jpg") as temp_file:
        temp_file.write(downloaded_file)
        temp_file.flush()

        with open(temp_file.name, "rb") as image_file:
            files = {"file": image_file}
            response = requests.patch(
                f"{api_url}/advertisers/{advertiser_id}/campaigns/{campaign_id}/image", files=files
            )

            data = response.json()

            if response.status_code == 200:
                return response.status_code, data

            if response.status_code == 422:
                return response.status_code, data["detail"][0]["msg"]

            return response.status_code, data["detail"]


def delete_campaign(advertiser_id, campaign_id):
    response = requests.delete(f"{api_url}/advertisers/{advertiser_id}/campaigns/{campaign_id}")

    if response.status_code == 204:
        return response.status_code, None

    data = response.json()

    if response.status_code == 422:
        return response.status_code, data["detail"][0]["msg"]

    return response.status_code, data["detail"]
