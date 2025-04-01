"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from sqlalchemy import and_

from src.api.advertisers.models import Advertiser, MlScore
from src.api.advertisers.schemas import AdvertiserSchema, MlScoreSchema
from src.db.deps import Session


def get_advertiser_by_id(advertiserId: uuid.UUID, session: Session) -> Advertiser:
    return session.query(Advertiser).filter(Advertiser.id == advertiserId).first()


def update_advertiser(advertiser_schema: AdvertiserSchema, session: Session) -> None:
    advertiser = session.query(Advertiser).filter(Advertiser.id == advertiser_schema.advertiser_id).first()
    if advertiser is None:
        advertiser = Advertiser(id=advertiser_schema.advertiser_id, name=advertiser_schema.name)
        session.add(advertiser)
    else:
        advertiser.name = advertiser_schema.name

    session.commit()


def advertiser_to_schema(advertiser: Advertiser) -> AdvertiserSchema:
    return AdvertiserSchema(advertiser_id=advertiser.id, name=advertiser.name)


def update_ml_score(ml_score_schema: MlScoreSchema, session: Session) -> None:
    ml_score = (
        session.query(MlScore)
        .filter(
            and_(MlScore.client_id == ml_score_schema.client_id, MlScore.advertiser_id == ml_score_schema.advertiser_id)
        )
        .first()
    )
    if ml_score is None:
        ml_score = MlScore(
            client_id=ml_score_schema.client_id,
            advertiser_id=ml_score_schema.advertiser_id,
            score=ml_score_schema.score,
        )
        session.add(ml_score)
    else:
        ml_score.score = ml_score_schema.score

    session.commit()


def get_advertisers(session: Session):
    advertiser = session.query(Advertiser).all()
    return advertiser
