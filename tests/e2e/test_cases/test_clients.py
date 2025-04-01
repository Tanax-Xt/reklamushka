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
from tests.e2e.utils import bulk_clients, get_client

client = TestClient(app)

GOOD_ID_1 = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
GOOD_ID_2 = "4ad85f64-5717-4562-b3fc-2c963f66afa6"
GOOD_LOGIN = "John Doe"
GOOD_AGE = 20
GOOD_LOCATION = "Moscow"
GOOD_GENDER = "MALE"


class TestClientBulk:
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
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    },
                    {
                        "client_id": GOOD_ID_2,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    },
                ],
                (200, 201),
            ),
        ],
    )
    def test_add_correct_client(self, data: list, status_code: tuple):
        response = bulk_clients(client, data)
        assert response.status_code in status_code

    @pytest.mark.parametrize(
        "data, status_code",
        [
            ([{}], 422),
            ([{"client_id": GOOD_ID_1}], 422),
            ([{"login": GOOD_LOGIN}], 422),
            ([{"age": GOOD_AGE}], 422),
            ([{"location": GOOD_LOCATION}], 422),
            ([{"gender": GOOD_GENDER}], 422),
            ([{"client_id": GOOD_ID_1, "login": GOOD_LOGIN}], 422),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": "Helicopter",
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": -1,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": 11,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": None,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": None,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": 123,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": 123,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": "пять",
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": False,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": "uuid",
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": None,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": None,
                        "location": GOOD_LOCATION,
                        "gender": GOOD_GENDER,
                    }
                ],
                422,
            ),
            (
                [
                    {
                        "client_id": GOOD_ID_1,
                        "login": GOOD_LOGIN,
                        "age": GOOD_AGE,
                        "location": GOOD_LOCATION,
                        "gender": None,
                    }
                ],
                422,
            ),
        ],
    )
    def test_add_incorrect_client(self, data: list, status_code: int):
        response = bulk_clients(client, data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "client_id, status_code",
        [
            ("", 404),
            (None, 422),
            (123, 422),
            (False, 422),
            ("bad-id", 422),
            ("58136458-8f3a-41a4-8e68-227650e6d4fd", 404),
        ],
    )
    def test_get_incorrect_client(self, client_id, status_code: int):
        response = get_client(client, client_id)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "client_id, status_code",
        [(GOOD_ID_1, 200), (GOOD_ID_2, 200)],
    )
    def test_get_correct_client(self, client_id, status_code: int):
        response = get_client(client, client_id)
        assert response.status_code == status_code
        assert response.json()["client_id"] == client_id
