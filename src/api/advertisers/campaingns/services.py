"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import tempfile
import uuid

from fastapi import UploadFile
from PIL import Image

from src.ai.moderation import send_moderation_response
from src.api.advertisers.campaingns.models import Campaign
from src.api.advertisers.campaingns.schemas import (
    CampaignCreateSchema,
    CampaignSchema,
    CampaignUpdateSchema,
    TargetingSchema,
)
from src.api.params import SearchParams
from src.config import settings
from src.date import get_current_date
from src.db.deps import Session
from src.moderation import get_current_moderation_state
from src.storage import s3_client


def add_campaign(
    advertiser_id: uuid.UUID,
    campaign_schema: CampaignCreateSchema | CampaignUpdateSchema,
    session: Session,
    campaign_id: uuid.UUID | None = None,
    image_url: str | None = None,
) -> Campaign:
    campaign = Campaign(
        advertiser_id=advertiser_id,
        impressions_limit=campaign_schema.impressions_limit,
        clicks_limit=campaign_schema.clicks_limit,
        cost_per_impression=campaign_schema.cost_per_impression,
        cost_per_click=campaign_schema.cost_per_click,
        ad_title=campaign_schema.ad_title,
        ad_text=campaign_schema.ad_text,
        start_date=campaign_schema.start_date,
        end_date=campaign_schema.end_date,
    )

    if campaign_id is not None:
        campaign.id = campaign_id

    if image_url is not None:
        campaign.image_url = image_url

    if campaign_schema.targeting is not None:
        campaign.gender = campaign_schema.targeting.gender
        campaign.age_from = campaign_schema.targeting.age_from
        campaign.age_to = campaign_schema.targeting.age_to
        campaign.location = campaign_schema.targeting.location

    session.add(campaign)
    session.commit()
    return campaign


def campaign_to_schema(campaign: Campaign) -> CampaignSchema:
    return CampaignSchema(
        campaign_id=campaign.id,
        advertiser_id=campaign.advertiser_id,
        impressions_limit=campaign.impressions_limit,
        clicks_limit=campaign.clicks_limit,
        cost_per_impression=campaign.cost_per_impression,
        cost_per_click=campaign.cost_per_click,
        ad_title=campaign.ad_title,
        ad_text=campaign.ad_text,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        image_url=get_image_url(campaign.image_url),
        targeting=TargetingSchema(
            gender=campaign.gender, age_from=campaign.age_from, age_to=campaign.age_to, location=campaign.location
        ),
    )


def is_campaign_active_on_current_date(campaign: Campaign) -> bool:
    current_date = get_current_date()
    if (
        (campaign.start_date is None and campaign.end_date is None)
        or (campaign.start_date <= current_date and campaign.end_date is None)
        or (campaign.end_date >= current_date and campaign.start_date is None)
        or (campaign.start_date <= current_date <= campaign.end_date)
    ):
        return True
    return False


def get_campaigns(advertiser_id: uuid.UUID, session: Session, search_params: SearchParams) -> list[Campaign]:
    return (
        session.query(Campaign)
        .filter(Campaign.advertiser_id == advertiser_id)
        .order_by(Campaign.created_at)
        .offset(search_params.size * (search_params.page - 1))
        .limit(search_params.size)
        .all()
    )


def get_campaign_by_id(campaign_id: uuid.UUID, session: Session) -> Campaign:
    return session.query(Campaign).filter(Campaign.id == campaign_id).first()


def update_campaign(campaign: Campaign, campaign_schema: CampaignUpdateSchema, session: Session) -> Campaign:
    advertiser_id = campaign.advertiser_id
    id = campaign.id
    image_url = campaign.image_url

    session.delete(campaign)
    session.commit()

    campaign = add_campaign(advertiser_id, campaign_schema, session, id, image_url)
    return campaign


def delete_campaign(campaign: Campaign, session: Session) -> None:
    session.delete(campaign)
    session.commit()


def get_image_from_file(file: UploadFile) -> Image.Image | None:
    # if not (file.content_type is not None and "image" in file.content_type):
    #     return None
    try:
        image = Image.open(file.file)
        return image
    except:
        return None


def add_image_to_s3(image: Image.Image) -> str:
    if image.mode == "RGBA":
        image = image.convert("RGB")

    name = uuid.uuid4().hex + ".jpeg"

    with tempfile.NamedTemporaryFile(delete=True, suffix=".jpeg") as temp_file:
        image.save(temp_file.name, format="JPEG")
        temp_file.flush()

        s3_client.fput_object(settings.MINIO_BUCKET_NAME, name, temp_file.name, content_type="image/jpeg")

    return name


def add_image_url_to_campaign(campaign: Campaign, image_path: str, session: Session) -> Campaign:
    if campaign.image_url is not None:
        s3_client.remove_object(settings.MINIO_BUCKET_NAME, campaign.image_url)

    campaign.image_url = image_path
    session.commit()
    session.refresh(campaign)

    return campaign


def get_image_url(image_url: str | None) -> str | None:
    if image_url is None:
        return None
    return settings.MINIO_PUBLIC_ADDRESS + "/" + settings.MINIO_BUCKET_NAME + "/" + image_url


def is_correct_text(title: str | None, text: str | None) -> (bool, str):
    if not get_current_moderation_state():
        return False, "Модерация рекламных кампаний отключена"

    if title is None:
        title = ""

    if text is None:
        text = ""

    verdict = send_moderation_response(f"{title}\n{text}")

    if verdict is None:
        return False, "Модерация отключена, произошла ошибка на стороне API"

    return verdict["block"], verdict["text"]


def get_all_campaigns(session: Session):
    campaign = session.query(Campaign).all()
    return campaign


def get_campaign_image(image_url: str) -> str:
    return s3_client.get_object(settings.MINIO_BUCKET_NAME, image_url)
