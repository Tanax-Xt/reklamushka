"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from sqlalchemy import and_

from src.api.ads.schemas import AdSchema
from src.api.ads.search_algorithm.choice import get_best_campaign, get_maxes
from src.api.ads.search_algorithm.filtering import limits_filtering, showing_filtering, target_and_date_filtering
from src.api.advertisers.campaingns.models import Campaign, ClientToCampaign
from src.api.advertisers.campaingns.services import get_image_url
from src.api.clients.models import Client
from src.date import get_current_date
from src.db.deps import Session


def get_best_campaign_for_client(client: Client, session: Session) -> Campaign | None:
    current_date = get_current_date()

    campaigns = target_and_date_filtering(current_date, client, session)
    if campaigns is None:
        return None

    campaigns_not_showed = showing_filtering(campaigns, client, session)
    if campaigns_not_showed is None:
        return campaigns.first()

    campaigns_without_exceeded_limits = limits_filtering(campaigns_not_showed, session)

    if campaigns_without_exceeded_limits is None:
        return None

    max_cost, max_ml_score = get_maxes(campaigns_without_exceeded_limits, client)

    best_campaign = get_best_campaign(campaigns_without_exceeded_limits, max_cost, max_ml_score, client, session)

    if best_campaign is None:
        return None

    register_show(current_date, best_campaign, client, session)

    return best_campaign


def register_show(current_date: int, campaign: Campaign, client: Client, session: Session):
    record = ClientToCampaign(
        campaign_id=campaign.id,
        client_id=client.id,
        cost_per_impression_for_client=campaign.cost_per_impression,
        date_show=current_date,
    )
    session.add(record)
    session.commit()


def is_campaign_active(campaign: Campaign) -> bool:
    current_date = get_current_date()
    if (
        (campaign.start_date is None and campaign.end_date is None)
        or (campaign.start_date <= current_date and campaign.end_date is None)
        or (campaign.end_date >= current_date and campaign.start_date is None)
        or (campaign.start_date <= current_date <= campaign.end_date)
    ):
        return True
    return False


def is_register_click(client: Client, campaign: Campaign, session: Session) -> bool:
    record = (
        session.query(ClientToCampaign)
        .filter(and_(ClientToCampaign.campaign_id == campaign.id, ClientToCampaign.client_id == client.id))
        .first()
    )

    if record is None:
        return False

    if record.is_click:
        return True

    record.is_click = True
    record.cost_per_click_for_client = campaign.cost_per_click
    record.date_click = get_current_date()

    session.commit()

    return True


def campaign_to_ad_schema(campaign: Campaign) -> AdSchema:
    return AdSchema(
        advertiser_id=campaign.advertiser_id,
        ad_id=campaign.id,
        ad_title=campaign.ad_title,
        ad_text=campaign.ad_text,
        image_url=get_image_url(campaign.image_url),
    )
