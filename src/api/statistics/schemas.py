"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from pydantic import BaseModel


class StatsSchema(BaseModel):
    impressions_count: int
    clicks_count: int
    conversion: float
    spent_impressions: float
    spent_clicks: float
    spent_total: float


class DailyStatsSchema(StatsSchema):
    date: int
