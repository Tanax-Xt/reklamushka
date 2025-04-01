"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound

from src.api.advertisers.campaingns.models import Campaign, ClientToCampaign
from src.api.advertisers.models import Advertiser
from src.api.statistics.services import join_daily_statistic
from src.db.deps import Session


def get_advertiser_statistics_metrics(advertiser: Advertiser, session: Session) -> tuple[int, int, float, float]:
    try:
        statistics = (
            session.query(
                func.count(ClientToCampaign.id).filter(ClientToCampaign.is_show.is_(True)).label("impressions_count"),
                func.count(ClientToCampaign.id).filter(ClientToCampaign.is_click.is_(True)).label("clicks_count"),
                func.coalesce(
                    func.sum(ClientToCampaign.cost_per_impression_for_client).filter(
                        ClientToCampaign.is_show.is_(True)
                    ),
                    0,
                ).label("spent_impressions"),
                func.coalesce(
                    func.sum(ClientToCampaign.cost_per_click_for_client).filter(ClientToCampaign.is_click.is_(True)), 0
                ).label("spent_clicks"),
            )
            .filter(
                ClientToCampaign.campaign_id.in_(
                    session.query(Campaign.id).filter(Campaign.advertiser_id == advertiser.id)
                )
            )
            .one()
        )
        return (
            statistics.impressions_count,
            statistics.clicks_count,
            statistics.spent_impressions,
            statistics.spent_clicks,
        )

    except NoResultFound:
        return 0, 0, 0, 0


def get_daily_advertiser_metrics(advertiser: Advertiser, session: Session) -> list[tuple[int, int, int, float, float]]:
    daily_statistics_impressions = (
        session.query(
            ClientToCampaign.date_show.label("date"),
            func.count(ClientToCampaign.id).filter(ClientToCampaign.is_show.is_(True)).label("impressions_count"),
            func.coalesce(
                func.sum(ClientToCampaign.cost_per_impression_for_client).filter(ClientToCampaign.is_show.is_(True)), 0
            ).label("spent_impressions"),
        )
        .filter(
            ClientToCampaign.campaign_id.in_(session.query(Campaign.id).filter(Campaign.advertiser_id == advertiser.id))
        )
        .group_by(ClientToCampaign.date_show)
        .order_by(ClientToCampaign.date_show)
        .all()
    )

    daily_statistics_clicks = (
        session.query(
            ClientToCampaign.date_click.label("date"),
            func.count(ClientToCampaign.id).filter(ClientToCampaign.is_click.is_(True)).label("clicks_count"),
            func.coalesce(
                func.sum(ClientToCampaign.cost_per_click_for_client).filter(ClientToCampaign.is_click.is_(True)), 0
            ).label("spent_clicks"),
        )
        .filter(
            ClientToCampaign.campaign_id.in_(session.query(Campaign.id).filter(Campaign.advertiser_id == advertiser.id))
        )
        .group_by(ClientToCampaign.date_click)
        .order_by(ClientToCampaign.date_click)
        .all()
    )

    return join_daily_statistic(daily_statistics_impressions, daily_statistics_clicks)
