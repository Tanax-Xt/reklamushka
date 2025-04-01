"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from src.api.advertisers.campaingns.schemas import CampaignCreateSchema, CampaignSchema, CampaignUpdateSchema
from src.api.advertisers.campaingns.services import (
    add_campaign,
    add_image_to_s3,
    add_image_url_to_campaign,
    campaign_to_schema,
    delete_campaign,
    get_campaign_by_id,
    get_campaign_image,
    get_campaigns,
    get_image_from_file,
    is_campaign_active_on_current_date,
    is_correct_text,
    update_campaign,
)
from src.api.advertisers.services import get_advertiser_by_id
from src.api.params import SearchParamsDepends
from src.date import is_date_correct
from src.db.deps import Session

campaign_router = APIRouter(prefix="/advertisers/{advertiserId}/campaigns", tags=["Campaigns"])


@campaign_router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_description="Рекламная кампания успешно создана.",
    response_model=CampaignSchema,
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser not found",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Start date may not be less than current date",
        },
        status.HTTP_424_FAILED_DEPENDENCY: {
            "description": "The advertising text did not pass moderation",
        },
    },
)
async def post_campaign(advertiserId: uuid.UUID, campaign_schema: CampaignCreateSchema, session: Session = Session):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    if not is_date_correct(campaign_schema.start_date):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Start date may not be less than current date")

    is_block, text = is_correct_text(campaign_schema.ad_title, campaign_schema.ad_text)
    if is_block:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=f"Реклама не прошла модерацию. {text}"
        )

    campaign = add_campaign(advertiserId, campaign_schema, session)

    return campaign_to_schema(campaign)


@campaign_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_description="Список рекламных кампаний рекламодателя.",
    response_model=list[CampaignSchema],
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser not found",
        },
    },
)
async def get_campaigns_with_pag(
    advertiserId: uuid.UUID, search_params: SearchParamsDepends, session: Session = Session
):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    campaigns = get_campaigns(advertiserId, session, search_params)
    return [campaign_to_schema(campaign) for campaign in campaigns]


@campaign_router.get(
    "/{campaignId}",
    status_code=status.HTTP_200_OK,
    response_description="Кампания успешно получена.",
    response_model=CampaignSchema,
    response_model_exclude_none=True,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Campaign does not belong to the advertiser",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser or Campaign not found",
        },
    },
)
async def get_campaign(advertiserId: uuid.UUID, campaignId: uuid.UUID, session: Session = Session):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    campaign = get_campaign_by_id(campaignId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if campaign.advertiser_id != advertiserId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Campaign does not belong to the advertiser")

    return campaign_to_schema(campaign)


@campaign_router.patch(
    "/{campaignId}/image",
    status_code=status.HTTP_200_OK,
    response_description="Изображение успешно обновлено",
    response_model=CampaignSchema,
    response_model_exclude_none=True,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Campaign does not belong to the advertiser",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser or Campaign not found",
        },
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {
            "description": "The uploaded file is not an image. Please upload an image file.",
        },
    },
)
async def add_image_to_campaign(
    advertiserId: uuid.UUID,
    campaignId: uuid.UUID,
    file: Optional[UploadFile] = File(),
    session: Session = Session,
):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    campaign = get_campaign_by_id(campaignId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if campaign.advertiser_id != advertiserId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Campaign does not belong to the advertiser")

    image = get_image_from_file(file)
    if not image:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "The uploaded file is not an image. Please upload an image file.",
        )

    image_path = add_image_to_s3(image)

    campaign = add_image_url_to_campaign(campaign, image_path, session)
    return campaign_to_schema(campaign)


@campaign_router.put(
    "/{campaignId}",
    status_code=status.HTTP_200_OK,
    response_description="Рекламная кампания успешно обновлена.",
    response_model=CampaignSchema,
    response_model_exclude_none=True,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Campaign does not belong to the advertiser",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser or Campaign not found",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Start date may not be less than current date or parameters that cannot be changed after the start of the campaign have been passed.",
        },
        status.HTTP_424_FAILED_DEPENDENCY: {
            "description": "The advertising text did not pass moderation",
        },
    },
)
async def put_campaign(
    advertiserId: uuid.UUID,
    campaignId: uuid.UUID,
    update_campaign_schema: CampaignUpdateSchema,
    session: Session = Session,
):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    campaign = get_campaign_by_id(campaignId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if campaign.advertiser_id != advertiserId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Campaign does not belong to the advertiser")

    if update_campaign_schema.start_date is not None and not is_date_correct(update_campaign_schema.start_date):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Start date may not be less than current date")

    if (
        update_campaign_schema.start_date is not None
        or update_campaign_schema.end_date is not None
        or update_campaign_schema.impressions_limit is not None
        or update_campaign_schema.clicks_limit is not None
    ) and is_campaign_active_on_current_date(campaign):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Parameters that cannot be changed after the start of the campaign have been passed.",
        )

    is_block, text = is_correct_text(update_campaign_schema.ad_title, update_campaign_schema.ad_text)
    if is_block:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=f"Реклама не прошла модерацию. {text}"
        )

    campaign = update_campaign(campaign, update_campaign_schema, session)

    return campaign_to_schema(campaign)


@campaign_router.delete(
    "/{campaignId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="	Рекламная кампания успешно удалена.",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Campaign does not belong to the advertiser",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser or Campaign not found",
        },
    },
)
async def remove_campaign(advertiserId: uuid.UUID, campaignId: uuid.UUID, session: Session = Session):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    campaign = get_campaign_by_id(campaignId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if campaign.advertiser_id != advertiserId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Campaign does not belong to the advertiser")

    delete_campaign(campaign, session)


@campaign_router.get(
    "/{campaignId}/image",
    status_code=status.HTTP_200_OK,
    response_description="Изображение успешно получено",
    response_model_exclude_none=True,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "There is no image for this campaign",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Campaign does not belong to the advertiser",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Advertiser or Campaign not found",
        },
    },
)
async def get_image_campaign(
    advertiserId: uuid.UUID,
    campaignId: uuid.UUID,
    session: Session = Session,
):
    advertiser = get_advertiser_by_id(advertiserId, session)

    if advertiser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertiser not found")

    campaign = get_campaign_by_id(campaignId, session)

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if campaign.advertiser_id != advertiserId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Campaign does not belong to the advertiser")

    if campaign.image_url is None:
        raise HTTPException(
            status.HTTP_204_NO_CONTENT,
            "There is no image for this campaign",
        )

    image = get_campaign_image(campaign.image_url)

    return StreamingResponse(image, media_type="image/jpeg")
