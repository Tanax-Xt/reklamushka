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
from tests.e2e.utils import update_date

client = TestClient(app)


class TestTime:
    @pytest.mark.parametrize(
        "data, status_code",
        [
            (
                {"current_date": "nine"},
                422,
            ),
            (
                {"current_date": -1},
                422,
            ),
        ],
    )
    def test_post_incorrect_date(self, data: dict, status_code: int):
        response = update_date(client, data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "status_code",
        [200],
    )
    def test_get_date(self, status_code: int):
        response = client.get("/time")
        assert response.status_code == status_code
