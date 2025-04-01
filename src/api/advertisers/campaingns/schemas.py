"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid
from enum import Enum
from typing import Optional, Self

from pydantic import BaseModel, confloat, conint, model_validator

from src.api.advertisers.schemas import AdvertiserIdSchema, ImageUrlSchema


class TargetGenderEnum(str, Enum):
    male = "MALE"
    female = "FEMALE"
    all = "ALL"


class TargetingSchema(BaseModel):
    gender: Optional[TargetGenderEnum] = "ALL"
    age_from: Optional[conint(ge=0)] = None
    age_to: Optional[conint(ge=0)] = None
    location: Optional[str] = None

    @model_validator(mode="after")
    def checks(self) -> Self:
        age_from = self.age_from
        age_to = self.age_to
        if age_from is not None and age_to is not None and age_to < age_from:
            raise ValueError("Age_to may not be less than age_from")

        return self


class CampaignCreateSchema(BaseModel):
    impressions_limit: conint(ge=0)
    clicks_limit: conint(ge=0)
    cost_per_impression: confloat(ge=0)
    cost_per_click: confloat(ge=0)
    ad_title: str
    ad_text: str
    start_date: conint(ge=0)
    end_date: conint(ge=0)
    targeting: Optional[TargetingSchema] = TargetingSchema()

    @model_validator(mode="after")
    def checks(self) -> Self:
        end = self.end_date
        start = self.start_date

        if (end is not None or start is not None) and (end < start):
            raise ValueError("End date may not be less than start date")

        impressions_limit = self.impressions_limit
        clicks_limit = self.clicks_limit
        if (impressions_limit is not None or clicks_limit is not None) and (clicks_limit > impressions_limit):
            raise ValueError("impressions_limit may not be less than clicks_limit")

        return self


class CampaignUpdateSchema(BaseModel):
    impressions_limit: Optional[conint(ge=0)] = 0
    clicks_limit: Optional[conint(ge=0)] = 0
    cost_per_impression: Optional[confloat(ge=0)] = 0
    cost_per_click: Optional[confloat(ge=0)] = 0
    ad_title: Optional[str] = None
    ad_text: Optional[str] = None
    start_date: Optional[conint(ge=0)] = None
    end_date: Optional[conint(ge=0)] = None
    targeting: Optional[TargetingSchema] = TargetingSchema()

    @model_validator(mode="after")
    def checks(self) -> Self:
        end = self.end_date
        start = self.start_date

        if (end is not None or start is not None) and (end < start):
            raise ValueError("End date may not be less than start date")

        impressions_limit = self.impressions_limit
        clicks_limit = self.clicks_limit
        if (impressions_limit is not None or clicks_limit is not None) and (clicks_limit > impressions_limit):
            raise ValueError("impressions_limit may not be less than clicks_limit")

        return self


class CampaignIdSchema(BaseModel):
    campaign_id: uuid.UUID


class CampaignSchema(CampaignIdSchema, AdvertiserIdSchema, CampaignUpdateSchema, ImageUrlSchema):
    targeting: TargetingSchema
