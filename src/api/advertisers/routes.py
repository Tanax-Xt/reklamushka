"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from fastapi import APIRouter, HTTPException, status

from src.api.advertisers.campaingns.schemas import CampaignIdSchema
from src.api.advertisers.campaingns.services import get_all_campaigns
from src.api.advertisers.schemas import AdvertiserIdSchema, AdvertiserSchema, MlScoreSchema
from src.api.advertisers.services import (
    advertiser_to_schema,
    get_advertiser_by_id,
    get_advertisers,
    update_advertiser,
    update_ml_score,
)
from src.api.clients.services import get_client_by_id
from src.db.deps import Session

advertiser_router = APIRouter(prefix="", tags=["Advertisers"])


@advertiser_router.get(
    "/advertisers/{advertiserId}",
    status_code=status.HTTP_200_OK,
    response_description="Информация о рекламодателе успешно получена.",
    response_model=AdvertiserSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser not found",
        },
    },
)
async def get_advertiser(advertiserId: uuid.UUID, session: Session = Session):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    return advertiser_to_schema(advertiser)


@advertiser_router.post(
    "/advertisers/bulk",
    status_code=status.HTTP_200_OK,
    response_description="Успешное создание/обновление рекламодателей",
    response_model=list[AdvertiserSchema],
)
async def bulk_advertisers(advertisers_list: list[AdvertiserSchema], session: Session = Session):
    for advertiser in advertisers_list:
        update_advertiser(advertiser, session)
    return advertisers_list


@advertiser_router.post(
    "/ml-scores",
    status_code=status.HTTP_200_OK,
    response_description="ML скор успешно добавлен или обновлён.",
    response_model=MlScoreSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser or Client not found",
        },
    },
)
async def ml_score(ml_score_schema: MlScoreSchema, session: Session = Session):
    advertiser = get_advertiser_by_id(ml_score_schema.advertiser_id, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    client = get_client_by_id(ml_score_schema.client_id, session)

    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    update_ml_score(ml_score_schema, session)

    return ml_score_schema


@advertiser_router.get(
    "/advertisers-ids",
    status_code=status.HTTP_200_OK,
    response_description="ID рекламодателей успешно получены",
    response_model=list[AdvertiserIdSchema],
)
async def get_advertisers_ids_for_statistics(session: Session = Session):
    advertisers = get_advertisers(session)
    return [AdvertiserIdSchema(advertiser_id=advertiser.id) for advertiser in advertisers]


@advertiser_router.get(
    "/campaigns-ids",
    status_code=status.HTTP_200_OK,
    response_description="ID рекламных кампаний успешно получены",
    response_model=list[CampaignIdSchema],
)
async def get_campaigns_ids_for_statistics(session: Session = Session):
    campaigns = get_all_campaigns(session)
    return [CampaignIdSchema(campaign_id=campaign.id) for campaign in campaigns]
