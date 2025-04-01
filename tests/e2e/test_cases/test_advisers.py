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
from tests.e2e.utils import add_ml_score, bulk_advertisers, bulk_clients, get_advertise

client = TestClient(app)

GOOD_ID_1 = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
GOOD_LOGIN = "John Doe"
GOOD_AGE = 20
GOOD_LOCATION = "Moscow"
GOOD_GENDER = "MALE"

GOOD_NAME = "John Doe inc"
GOOD_ID_2 = "4ad85f64-5717-4562-b3fc-2c963f66afa6"


class TestAdvisers:
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
            )
        ],
    )
    def test_add_correct_client(self, data: list, status_code: tuple):
        response = bulk_clients(client, data)
        assert response.status_code in status_code

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
            ),
            (
                [
                    {
                        "advertiser_id": GOOD_ID_1,
                        "name": GOOD_NAME + "2",
                    },
                    {
                        "advertiser_id": GOOD_ID_2,
                        "name": GOOD_NAME,
                    },
                ],
                (200, 201),
            ),
        ],
    )
    def test_add_correct_advisers(self, data: list, status_code: tuple):
        response = bulk_advertisers(client, data)
        assert response.status_code in status_code
        assert response.json()[0]["name"] == data[0]["name"]

    @pytest.mark.parametrize(
        "data, status_code",
        [
            (
                [{}],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": GOOD_ID_1,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "name": GOOD_NAME,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": GOOD_ID_1,
                        "name": 123,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": GOOD_ID_1,
                        "name": None,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": GOOD_ID_1,
                        "name": False,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": None,
                        "name": GOOD_NAME,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": False,
                        "name": GOOD_NAME,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": 123,
                        "name": GOOD_NAME,
                    },
                ],
                422,
            ),
            (
                [
                    {
                        "advertiser_id": "bad-id",
                        "name": GOOD_NAME,
                    },
                ],
                422,
            ),
        ],
    )
    def test_add_incorrect_advisers(self, data: list, status_code: int):
        response = bulk_advertisers(client, data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "advertiser_id, status_code",
        [
            ("", 404),
            (None, 422),
            (123, 422),
            (False, 422),
            ("bad-id", 422),
            ("58136458-8f3a-41a4-8e68-227650e6d4fd", 404),
        ],
    )
    def test_get_incorrect_adviser(self, advertiser_id, status_code: int):
        response = get_advertise(client, advertiser_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "advertiser_id, status_code",
        [(GOOD_ID_1, (200, 201)), (GOOD_ID_2, (200, 201))],
    )
    def test_get_correct_adviser(self, advertiser_id, status_code: tuple):
        response = get_advertise(client, advertiser_id)
        assert response.status_code in status_code
        assert response.json()["advertiser_id"] == advertiser_id

    @pytest.mark.parametrize(
        "data, status_code",
        [
            ({}, 422),
            ({"advertiser_id": GOOD_ID_1}, 422),
            ({"client_id": GOOD_ID_1}, 422),
            ({"score": 0}, 422),
            ({"advertiser_id": GOOD_ID_1, "client_id": GOOD_ID_1}, 422),
            ({"advertiser_id": GOOD_ID_1, "score": 0}, 422),
            ({"score": 0, "client_id": GOOD_ID_1}, 422),
            ({"advertiser_id": GOOD_ID_1, "client_id": GOOD_ID_1, "score": -1}, 422),
            ({"advertiser_id": GOOD_ID_1, "client_id": GOOD_ID_1, "score": None}, 422),
            ({"advertiser_id": "58136458-8f3a-41a4-8e68-227650e6d4fd", "client_id": GOOD_ID_1, "score": 1}, 404),
            ({"advertiser_id": GOOD_ID_1, "client_id": "58136458-8f3a-41a4-8e68-227650e6d4fd", "score": 1}, 404),
        ],
    )
    def test_add_incorrect_ml_score(self, data: dict, status_code: int):
        response = add_ml_score(client, data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "data, status_code",
        [
            ({"advertiser_id": GOOD_ID_1, "client_id": GOOD_ID_1, "score": 1}, 200),
            ({"advertiser_id": GOOD_ID_2, "client_id": GOOD_ID_1, "score": 1}, 200),
            ({"advertiser_id": GOOD_ID_1, "client_id": GOOD_ID_1, "score": 2}, 200),
        ],
    )
    def test_add_correct_ml_score(self, data: list, status_code: int):
        response = add_ml_score(client, data)
        assert response.status_code == status_code
        assert response.json()["score"] == data["score"]
