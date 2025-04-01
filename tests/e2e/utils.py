"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from fastapi.responses import Response
from fastapi.testclient import TestClient


def bulk_clients(client: TestClient, clients: list) -> Response:
    response = client.post("/clients/bulk", json=clients)
    return response


def get_client(client: TestClient, client_id: str) -> Response:
    response = client.get(f"/clients/{client_id}")
    return response


def bulk_advertisers(client: TestClient, advertisers: list) -> Response:
    response = client.post("/advertisers/bulk", json=advertisers)
    return response


def get_advertise(client: TestClient, advertiser_id: str) -> Response:
    response = client.get(f"/advertisers/{advertiser_id}")
    return response


def add_ml_score(client: TestClient, data: dict) -> Response:
    response = client.post("/ml-scores", json=data)
    return response


def post_campaign(client: TestClient, advertiser_id: str, data: dict) -> Response:
    response = client.post(f"/advertisers/{advertiser_id}/campaigns", json=data)
    return response


def get_campaigns(client: TestClient, advertiser_id: str) -> Response:
    response = client.get(f"/advertisers/{advertiser_id}/campaigns")
    return response


def get_campaign(client: TestClient, advertiser_id: str, campaign_id: str) -> Response:
    response = client.get(f"/advertisers/{advertiser_id}/campaigns/{campaign_id}")
    return response


def get_ad(client: TestClient, client_id: str) -> Response:
    response = client.get(f"/ads?client_id={client_id}")
    return response


def click_ad(client: TestClient, ad_id: str, client_id: str) -> Response:
    response = client.post(f"/ads/{ad_id}/click", json={"client_id": client_id})
    return response


def get_statistics_advertiser(client: TestClient, advertiser_id: str, daily: str = "") -> Response:
    response = client.get(f"stats/advertisers/{advertiser_id}/campaigns{daily}")
    return response


def get_statistics_campaign(client: TestClient, campaign_id: str, daily: str = "") -> Response:
    response = client.get(f"stats/campaigns/{campaign_id}{daily}")
    return response


def update_date(client: TestClient, data: dict) -> Response:
    response = client.post("/time/advance", json=data)
    return response


def generate_text(client: TestClient, data: dict) -> Response:
    response = client.post("/ai/generate-text", json=data)
    return response


def moderation_state(client: TestClient, data: dict) -> Response:
    response = client.post("/ai/moderation-campaigns", json=data)
    return response
