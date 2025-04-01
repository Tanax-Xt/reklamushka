"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from fastapi import APIRouter, HTTPException, status

from src.api.advertisers.services import get_advertiser_by_id
from src.api.statistics.advertisers.services import get_advertiser_statistics_metrics, get_daily_advertiser_metrics
from src.api.statistics.schemas import DailyStatsSchema, StatsSchema
from src.api.statistics.services import daily_metrics_to_schema, metrics_to_schema
from src.db.deps import Session

advertisers_statistics_router = APIRouter(prefix="/stats/advertisers/{advertiserId}/campaigns", tags=["Statistics"])


@advertisers_statistics_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_description="Агрегированная статистика по всем кампаниям рекламодателя успешно получена.",
    response_model=StatsSchema,
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser not found",
        },
    },
)
async def get_advertisers_statistics(advertiserId: uuid.UUID, session: Session = Session):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    impressions_count, clicks_count, spent_impressions, spent_clicks = get_advertiser_statistics_metrics(
        advertiser, session
    )

    return metrics_to_schema(impressions_count, clicks_count, spent_impressions, spent_clicks)


@advertisers_statistics_router.get(
    "/daily",
    status_code=status.HTTP_200_OK,
    response_description="Ежедневная агрегированная статистика успешно получена.",
    response_model=list[DailyStatsSchema],
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser not found",
        },
    },
)
async def get_daily_advertisers_statistics(advertiserId: uuid.UUID, session: Session = Session):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    metrics = get_daily_advertiser_metrics(advertiser, session)

    return daily_metrics_to_schema(metrics)
