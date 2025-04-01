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
from tests.e2e.utils import bulk_advertisers, get_statistics_advertiser, get_statistics_campaign, post_campaign

client = TestClient(app)

GOOD_NAME = "John Doe inc"
GOOD_ID_1 = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
BAD_ID_2 = "3fa85f64-5717-4562-b3fc-2c963f66afa7"


class TestStatistics:
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
        "advertiser_id, status_code",
        [(BAD_ID_2, 404)],
    )
    def test_get_incorrect_statistics(self, advertiser_id: str, status_code: int):
        response = get_statistics_advertiser(client, advertiser_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "advertiser_id, status_code",
        [(BAD_ID_2, 404)],
    )
    def test_get_incorrect_daily_statistics(self, advertiser_id: str, status_code: int):
        response = get_statistics_advertiser(client, advertiser_id, "/daily")
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "advertiser_id, status_code",
        [(GOOD_ID_1, 200)],
    )
    def test_get_correct_statistics(self, advertiser_id: str, status_code: int):
        response = get_statistics_advertiser(client, advertiser_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "advertiser_id, status_code",
        [(GOOD_ID_1, 200)],
    )
    def test_get_correct_daily_statistics(self, advertiser_id: str, status_code: int):
        response = get_statistics_advertiser(client, advertiser_id, "/daily")
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "campaign_id, status_code",
        [(BAD_ID_2, 404)],
    )
    def test_get_incorrect_statistics(self, campaign_id: str, status_code: int):
        response = get_statistics_campaign(client, campaign_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "campaign_id, status_code",
        [(BAD_ID_2, 404)],
    )
    def test_get_incorrect_daily_statistics(self, campaign_id: str, status_code: int):
        response = get_statistics_campaign(client, campaign_id, "/daily")
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "data, advertiser_id, status_code",
        [
            (
                {
                    "impressions_limit": 0,
                    "clicks_limit": 0,
                    "cost_per_impression": 0,
                    "cost_per_click": 0,
                    "ad_title": "string",
                    "ad_text": "string",
                    "start_date": 0,
                    "end_date": 0,
                },
                GOOD_ID_1,
                200,
            ),
        ],
    )
    def test_get_correct_statistics(self, data: dict, advertiser_id: str, status_code: int):
        campaign_id = post_campaign(client, advertiser_id, data).json()["campaign_id"]
        response = get_statistics_campaign(client, campaign_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "data, advertiser_id, status_code",
        [
            (
                {
                    "impressions_limit": 0,
                    "clicks_limit": 0,
                    "cost_per_impression": 0,
                    "cost_per_click": 0,
                    "ad_title": "string",
                    "ad_text": "string",
                    "start_date": 0,
                    "end_date": 0,
                },
                GOOD_ID_1,
                200,
            ),
        ],
    )
    def test_get_correct_statistics(self, data: dict, advertiser_id: str, status_code: int):
        campaign_id = post_campaign(client, advertiser_id, data).json()["campaign_id"]
        response = get_statistics_campaign(client, campaign_id, "/daily")
        assert response.status_code == status_code
