"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import pytest
from fastapi.testclient import TestClient

from src.app import app
from tests.e2e.utils import bulk_advertisers, bulk_clients, click_ad, get_ad, post_campaign

client = TestClient(app)

GOOD_impressions_limit = 10
GOOD_clicks_limit = 6
GOOD_GENDER = "MALE"

GOOD_NAME = "John Doe inc"
GOOD_ID_1 = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
BAD_ID_1 = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
GOOD_LOGIN = "John Doe"
GOOD_AGE = 20
GOOD_LOCATION = "Moscow"


class TestCampaigns:
    @pytest.mark.parametrize(
        "data, status_code",
        [
            (
                [
                    {
                        "advertiser_id": GOOD_ID_1,
                        "name": GOOD_NAME,
                    }
                ],
                (200, 201),
            )
        ],
    )
    def test_add_correct_advisers(self, data: list, status_code: tuple):
        response = bulk_advertisers(client, data)
        assert response.status_code in status_code

    @pytest.mark.parametrize(
        "data, status_code",
        [
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                (200, 201),
            ),
        ],
    )
    def test_add_correct_client(self, data: list, status_code: tuple):
        response = bulk_clients(client, data)
        assert response.status_code in status_code

    @pytest.mark.parametrize(
        "data, client_id, advertiser_id, status_code",
        [
            (
                {
                    "impressions_limit": GOOD_impressions_limit,
                    "clicks_limit": GOOD_clicks_limit,
                    "cost_per_impression": 0,
                    "cost_per_click": 0,
                    "ad_title": "string",
                    "ad_text": "string",
                    "start_date": 0,
                    "end_date": 0,
                    "targeting": {"gender": GOOD_GENDER},
                },
                GOOD_ID_1,
                "123",
                404,
            ),
            (
                {
                    "impressions_limit": GOOD_impressions_limit,
                    "clicks_limit": GOOD_clicks_limit,
                    "cost_per_impression": 0,
                    "cost_per_click": 0,
                    "ad_title": "string",
                    "ad_text": "string",
                    "start_date": 0,
                    "end_date": 0,
                    "targeting": {"gender": GOOD_GENDER},
                },
                BAD_ID_1,
                GOOD_ID_1,
                404,
            ),
        ],
    )
    def test_get_incorrect_ads(self, data: dict, client_id: str, advertiser_id: str, status_code: int):
        post_campaign(client, advertiser_id, data)
        response = get_ad(client, client_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "client_id, status_code",
        [
            (
                GOOD_ID_1,
                200,
            )
        ],
    )
    def test_get_correct_ads(self, client_id: str, status_code: int):
        response = get_ad(client, client_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "client_id, status_code",
        [
            (
                GOOD_ID_1,
                204,
            )
        ],
    )
    def test_get_correct_click(self, client_id: str, status_code: int):
        ad_id = get_ad(client, client_id).json()["ad_id"]
        response = click_ad(client, ad_id, client_id)
        assert response.status_code == status_code
