"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from pydantic import conint


@dataclass
class SearchParams:
    size: conint(ge=0) = 10
    page: conint(ge=1) = 1


SearchParamsDepends = Annotated[SearchParams, Depends(SearchParams)]
