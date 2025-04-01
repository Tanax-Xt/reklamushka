"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from fastapi import APIRouter, HTTPException, status

from src.api.time.schemas import DateSchema
from src.date import get_current_date, is_date_correct, set_current_date

time_router = APIRouter(prefix="/time", tags=["Time"])


@time_router.post(
    "/advance",
    status_code=status.HTTP_200_OK,
    response_description="Текущая дата обновлена",
    response_model=DateSchema,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Date may not be less than current date",
        },
    },
)
async def post_date(date_schema: DateSchema = None):
    if date_schema is None:
        current_date = get_current_date() + 1
    else:
        if not is_date_correct(date_schema.current_date):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Date may not be less than current date")
        current_date = date_schema.current_date

    set_current_date(current_date)
    return DateSchema(current_date=current_date)


@time_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_description="Текущая дата",
    response_model=DateSchema,
)
async def get_date():
    return DateSchema(current_date=get_current_date())
