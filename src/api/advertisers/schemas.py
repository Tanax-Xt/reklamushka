"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid
from typing import Optional

from pydantic import BaseModel, conint

from src.api.clients.schemas import ClientIdSchema


class ImageUrlSchema(BaseModel):
    image_url: Optional[str] = None


class AdvertiserIdSchema(BaseModel):
    advertiser_id: uuid.UUID


class AdvertiserSchema(AdvertiserIdSchema):
    name: str


class MlScoreSchema(AdvertiserIdSchema, ClientIdSchema):
    score: conint(ge=0)
