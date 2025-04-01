from fastapi import APIRouter

from src.api.ads import ads_router
from src.api.advertisers import advertiser_router
from src.api.advertisers.campaingns import campaign_router
from src.api.ai import ai_router
from src.api.clients import client_router
from src.api.statistics import advertisers_statistics_router, campaign_statistics_router
from src.api.time import time_router

api_router = APIRouter()
api_router.include_router(ai_router)
api_router.include_router(client_router)
api_router.include_router(advertiser_router)
api_router.include_router(campaign_router)
api_router.include_router(ads_router)
api_router.include_router(advertisers_statistics_router)
api_router.include_router(campaign_statistics_router)
api_router.include_router(time_router)

__all__ = [
    "api_router",
]
