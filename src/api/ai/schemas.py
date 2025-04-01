"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from typing import Optional

from pydantic import BaseModel


class ModerationStateSchema(BaseModel):
    current_state: bool


class TextGeneratingRequest(BaseModel):
    product: str
    advertiser_name: str
    audience: Optional[str] = "охвати как можно больше людей"
    target: Optional[str] = "покупка"


class GeneratedTextSchema(BaseModel):
    title: str
    text: str
