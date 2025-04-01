from sqlalchemy import and_, case, func

from src.api.advertisers.campaingns.models import Campaign, ClientToCampaign
from src.api.advertisers.models import MlScore
from src.api.clients.models import Client
from src.db.deps import Session


def get_maxes(campaigns, client: Client):
    """Return max_cost and max_ml_score"""

    max_cost = campaigns.with_entities(
        func.max(func.coalesce(Campaign.cost_per_impression, 1) + func.coalesce(Campaign.cost_per_impression, 1))
    ).scalar()

    max_ml_score = (
        campaigns.outerjoin(
            MlScore, and_(Campaign.advertiser_id == MlScore.advertiser_id, client.id == MlScore.client_id)
        )
        .with_entities(func.coalesce(func.max(MlScore.score), 1))
        .scalar()
    )

    if not max_cost:
        max_cost = 1
    if not max_ml_score:
        max_ml_score = 1

    return max_cost, max_ml_score


def get_best_campaign(campaigns, max_cost: int, max_ml_score: int, client: Client, session: Session) -> Campaign | None:
    stats_subquery = (
        session.query(
            ClientToCampaign.campaign_id.label("campaign_id"),
            func.count(case((ClientToCampaign.is_show, True))).label("impressions"),
            func.count(case((ClientToCampaign.is_click, True))).label("clicks"),
        )
        .group_by(ClientToCampaign.campaign_id)
        .subquery()
    )

    query = (
        campaigns.outerjoin(stats_subquery, Campaign.id == stats_subquery.c.campaign_id)
        .outerjoin(MlScore, and_(Campaign.advertiser_id == MlScore.advertiser_id, MlScore.client_id == client.id))
        .add_columns(
            func.coalesce(MlScore.score, 0).label("ml_score"),
            func.coalesce(stats_subquery.c.impressions, 0).label("impressions"),
            func.coalesce(stats_subquery.c.clicks, 0).label("clicks"),
        )
    )

    penalty_impressions = case(
        (
            and_(Campaign.impressions_limit.isnot(None), Campaign.impressions_limit != 0),
            (func.coalesce(stats_subquery.c.impressions, 0) - Campaign.impressions_limit) / Campaign.impressions_limit,
        ),
        else_=0,
    )
    penalty_clicks = case(
        (
            and_(Campaign.clicks_limit.isnot(None), Campaign.clicks_limit != 0),
            (func.coalesce(stats_subquery.c.clicks, 0) - Campaign.clicks_limit) / Campaign.clicks_limit,
        ),
        else_=0,
    )

    score_expr = (
        0.25 * (func.coalesce(MlScore.score, 0) / max_ml_score)
        + 0.65
        * (
            (Campaign.cost_per_impression + Campaign.cost_per_click * (func.coalesce(MlScore.score, 0) / max_ml_score))
            / max_cost
        )
        # - 0.5 * (penalty_impressions + penalty_clicks)
        - 0.75 * (penalty_impressions + penalty_clicks)
    ).label("score")

    query = query.add_columns(score_expr).order_by(score_expr.desc())

    best = query.first()
    if best:
        # best – кортеж: (Campaign, ml_score, impressions, clicks, score)
        return best[0]
    return None
