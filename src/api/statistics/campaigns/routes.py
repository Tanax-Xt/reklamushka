"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from fastapi import APIRouter, HTTPException, status

from src.api.advertisers.campaingns.services import get_campaign_by_id
from src.api.statistics.campaigns.services import get_campaign_statistics_metrics, get_daily_campaign_metrics
from src.api.statistics.schemas import DailyStatsSchema, StatsSchema
from src.api.statistics.services import daily_metrics_to_schema, metrics_to_schema
from src.db.deps import Session

campaign_statistics_router = APIRouter(prefix="/stats/campaigns/{campaignId}", tags=["Statistics"])


@campaign_statistics_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_description="Статистика по рекламной кампании успешно получена.",
    response_model=StatsSchema,
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Campaign not found",
        },
    },
)
async def get_campaign_statistics(campaignId: uuid.UUID, session: Session = Session):
    campaign = get_campaign_by_id(campaignId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    impressions_count, clicks_count, spent_impressions, spent_clicks = get_campaign_statistics_metrics(
        campaign, session
    )

    return metrics_to_schema(impressions_count, clicks_count, spent_impressions, spent_clicks)


@campaign_statistics_router.get(
    "/daily",
    status_code=status.HTTP_200_OK,
    response_description="Ежедневная статистика по рекламной кампании успешно получена.",
    response_model=list[DailyStatsSchema],
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Campaign not found",
        },
    },
)
async def get_daily_campaign_statistics(campaignId: uuid.UUID, session: Session = Session):
    campaign = get_campaign_by_id(campaignId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    metrics = get_daily_campaign_metrics(campaign, session)

    return daily_metrics_to_schema(metrics)
