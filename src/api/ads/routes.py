"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from fastapi import APIRouter, HTTPException, status

from src.api.ads.schemas import AdSchema
from src.api.ads.services import (
    campaign_to_ad_schema,
    get_best_campaign_for_client,
    is_register_click,
)
from src.api.advertisers.campaingns.services import get_campaign_by_id, is_campaign_active_on_current_date
from src.api.clients.schemas import ClientIdSchema
from src.api.clients.services import get_client_by_id
from src.db.deps import Session

ads_router = APIRouter(prefix="/ads", tags=["Ads"])


@ads_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_description="Рекламное объявление успешно возвращено.",
    response_model=AdSchema,
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Ad or Client not found",
        },
    },
)
async def get_ad(client_id: uuid.UUID, session: Session = Session):
    client = get_client_by_id(client_id, session)

    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    campaign = get_best_campaign_for_client(client, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")

    return campaign_to_ad_schema(campaign)


@ads_router.post(
    "/{adId}/click",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Переход по рекламному объявлению успешно зафиксирован.",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Does not take place on the current date",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Ad or Client not found",
        },
        status.HTTP_409_CONFLICT: {
            "description": "This ad was not shown to the user",
        },
    },
)
async def post_click(adId: uuid.UUID, client_id_schema: ClientIdSchema, session: Session = Session):
    client = get_client_by_id(client_id_schema.client_id, session)

    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    campaign = get_campaign_by_id(adId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")

    if not is_campaign_active_on_current_date(campaign):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Does not take place on the current date")

    is_click = is_register_click(client, campaign, session)

    if is_click is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This ad was not shown to the user")
