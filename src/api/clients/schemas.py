"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid
from enum import Enum

from pydantic import BaseModel, conint


class ClientIdSchema(BaseModel):
    client_id: uuid.UUID


class GenderEnum(str, Enum):
    male = "MALE"
    female = "FEMALE"


class ClientSchema(ClientIdSchema):
    login: str
    age: conint(ge=0)
    location: str
    gender: GenderEnum
