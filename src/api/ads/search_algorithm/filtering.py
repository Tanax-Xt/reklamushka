from sqlalchemy import and_, case, func, or_

from src.api.advertisers.campaingns.models import Campaign, ClientToCampaign
from src.api.clients.models import Client
from src.db.deps import Session


def target_and_date_filtering(current_date: int, client: Client, session: Session):
    campaigns = (
        session.query(Campaign)
        .filter(
            or_(
                and_(Campaign.age_to.is_(None), Campaign.age_from.is_(None)),
                and_(Campaign.age_from <= client.age, Campaign.age_to.is_(None)),
                and_(Campaign.age_to >= client.age, Campaign.age_from.is_(None)),
                and_(Campaign.age_from <= client.age, Campaign.age_to >= client.age),
            )
        )
        .filter(or_(Campaign.location.is_(None), Campaign.location == client.location))
        .filter(or_(Campaign.gender.is_(None), Campaign.gender == "ALL", Campaign.gender == client.gender))
        .filter(
            or_(
                and_(Campaign.start_date.is_(None), Campaign.end_date.is_(None)),
                and_(Campaign.start_date <= current_date, Campaign.end_date.is_(None)),
                and_(Campaign.end_date >= current_date, Campaign.start_date.is_(None)),
                and_(Campaign.start_date <= current_date, Campaign.end_date >= current_date),
            )
        )
    )

    if not campaigns.all():
        return None

    return campaigns


def showing_filtering(campaigns, client: Client, session: Session):
    # Какие объявления были показаны
    showed_campaigns_ids = session.query(ClientToCampaign.campaign_id).filter(ClientToCampaign.client_id == client.id)

    campaigns_not_showed = campaigns.filter(~Campaign.id.in_(showed_campaigns_ids))

    if not campaigns_not_showed.all():
        # Если все объявления были показаны, вернем None
        return None

    return campaigns_not_showed


def limits_filtering(campaigns_not_showed, session: Session):
    stats_subquery = (
        session.query(
            ClientToCampaign.campaign_id,
            func.count(case((ClientToCampaign.is_show, True))).label("impressions"),
            func.count(case((ClientToCampaign.is_click, True))).label("clicks"),
        )
        .group_by(ClientToCampaign.campaign_id)
        .subquery()
    )

    # Основной запрос: берем кампании из campaigns_not_showed, присоединяем статистику
    query = campaigns_not_showed.outerjoin(stats_subquery, Campaign.id == stats_subquery.c.campaign_id).filter(
        # Если лимит показов есть, то показы не должны превышать лимит * 1.5, иначе условие проходит
        or_(
            Campaign.impressions_limit.is_(None),
            func.coalesce(stats_subquery.c.impressions + 1, 0) <= Campaign.impressions_limit * 1.5,
        ),
        # Аналогично для кликов
        # or_(
        #     Campaign.clicks_limit.is_(None),
        #     func.coalesce(stats_subquery.c.clicks + 1, 0) <= Campaign.clicks_limit * 1.5,
        # ),
    )

    campaigns_without_exceeded_limits = query

    # Если ни одна кампания не удовлетворяет условию, возвращаем все кампании
    if not campaigns_without_exceeded_limits.all():
        # campaigns_without_exceeded_limits = campaigns_not_showed
        return None

    return campaigns_without_exceeded_limits
