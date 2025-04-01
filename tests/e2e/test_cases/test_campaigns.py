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
from tests.e2e.utils import bulk_advertisers, get_campaign, get_campaigns, post_campaign

client = TestClient(app)

GOOD_impressions_limit = 10
GOOD_clicks_limit = 6
GOOD_GENDER = "MALE"

GOOD_NAME = "John Doe inc"
GOOD_ID_1 = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
BAD_ID_2 = "3fa85f64-5717-4562-b3fc-2c963f66afa7"


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
    def test_add_correct_advisers(self, data: list, status_code: int):
        response = bulk_advertisers(client, data)
        assert response.status_code in status_code

    @pytest.mark.parametrize(
        "data, advertiser_id, status_code",
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
                BAD_ID_2,
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
                    "targeting": {"gender": "Helicopter"},
                },
                GOOD_ID_1,
                422,
            ),
            (
                {
                    "impressions_limit": GOOD_impressions_limit,
                    "clicks_limit": GOOD_clicks_limit,
                    "cost_per_impression": 0,
                    "cost_per_click": 0,
                    "ad_title": "string",
                    "ad_text": "string",
                    "start_date": 3,
                    "end_date": 2,
                },
                GOOD_ID_1,
                422,
            ),
            (
                {
                    "impressions_limit": 2,
                    "clicks_limit": 3,
                    "cost_per_impression": 0,
                    "cost_per_click": 0,
                    "ad_title": "string",
                    "ad_text": "string",
                    "start_date": 1,
                    "end_date": 2,
                    "targeting": {"gender": GOOD_GENDER},
                },
                GOOD_ID_1,
                422,
            ),
        ],
    )
    def test_post_incorrect_campaign(self, data: dict, advertiser_id: str, status_code: int):
        response = post_campaign(client, advertiser_id, data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "data, advertiser_id, status_code",
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
                (200, 201),
            ),
        ],
    )
    def test_post_correct_campaign(self, data: dict, advertiser_id: str, status_code: tuple):
        response = post_campaign(client, advertiser_id, data)
        assert response.status_code in status_code

    @pytest.mark.parametrize(
        "advertiser_id, status_code",
        [(BAD_ID_2, 404), ("id", 422), (12345, 422)],
    )
    def test_incorrect_get_campaigns(self, advertiser_id: str, status_code: int):
        response = get_campaigns(client, advertiser_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "advertiser_id, status_code",
        [(GOOD_ID_1, 200)],
    )
    def test_correct_get_campaigns(self, advertiser_id: str, status_code: int):
        response = get_campaigns(client, advertiser_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "advertiser_id, campaign_id, status_code",
        [(GOOD_ID_1, BAD_ID_2, 404), (GOOD_ID_1, 124, 422)],
    )
    def test_incorrect_get_campaign(self, advertiser_id: str, campaign_id: str, status_code: int):
        response = get_campaign(client, advertiser_id, campaign_id)
        assert response.status_code == status_code
