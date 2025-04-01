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
from tests.e2e.utils import (
    generate_text,
    moderation_state,
)

client = TestClient(app)

GOOD_TITLE = "Новая коллекция пельменей"
GOOD_NAME = "Кафе 'Вкуснотища'"


class TestCampaigns:
    @pytest.mark.parametrize(
        "data, status_code",
        [
            (
                {
                    "product": GOOD_TITLE,
                    "advertiser_name": GOOD_NAME,
                },
                200,
            )
        ],
    )
    def test_add_correct_text_generate(self, data: dict, status_code: int):
        response = generate_text(client, data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "data, status_code",
        [
            (
                {
                    "product": GOOD_TITLE,
                },
                422,
            )
        ],
    )
    def test_add_incorrect_text_generate(self, data: dict, status_code: int):
        response = generate_text(client, data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "data, status_code",
        [
            (
                {
                    "current_state": "on",
                },
                422,
            )
        ],
    )
    def test_add_incorrect_moderation_state(self, data: dict, status_code: int):
        response = moderation_state(client, data)
        assert response.status_code == status_code
