"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
from src.db.mixins import AuditMixin


class Campaign(Base, AuditMixin):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    advertiser_id: Mapped[str] = mapped_column(ForeignKey("advertiser.id", ondelete="SET NULL"))
    impressions_limit: Mapped[int] = mapped_column(nullable=True)
    clicks_limit: Mapped[int] = mapped_column(nullable=True)
    cost_per_impression: Mapped[float] = mapped_column(nullable=True)
    cost_per_click: Mapped[float] = mapped_column(nullable=True)
    ad_title: Mapped[str] = mapped_column(nullable=True)
    ad_text: Mapped[str] = mapped_column(nullable=True)
    start_date: Mapped[int] = mapped_column(nullable=True)
    end_date: Mapped[int] = mapped_column(nullable=True)

    gender: Mapped[str] = mapped_column(nullable=True)
    age_from: Mapped[int] = mapped_column(nullable=True)
    age_to: Mapped[int] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)

    image_url: Mapped[str] = mapped_column(nullable=True)


class ClientToCampaign(Base, AuditMixin):
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    campaign_id: Mapped[str] = mapped_column(ForeignKey("campaign.id", ondelete="SET NULL"))
    client_id: Mapped[str] = mapped_column(ForeignKey("client.id", ondelete="SET NULL"))
    is_show: Mapped[bool] = mapped_column(default=True)
    is_click: Mapped[bool] = mapped_column(default=False)
    cost_per_impression_for_client: Mapped[int] = mapped_column()
    cost_per_click_for_client: Mapped[int] = mapped_column(default=None, nullable=True)
    date_show: Mapped[int] = mapped_column()
    date_click: Mapped[int] = mapped_column(default=None, nullable=True)
