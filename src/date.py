"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from src.cache import redis
from src.config import settings


def date_initialization(prefix=settings.DATE_PREFIX):
    if redis.get(prefix) is None:
        set_current_date(0, prefix)


def get_current_date(prefix=settings.DATE_PREFIX):
    return int(redis.get(prefix))


def set_current_date(date: int, prefix=settings.DATE_PREFIX):
    redis.set(prefix, date)


def is_date_correct(date: int, prefix=settings.DATE_PREFIX):
    cur_date = get_current_date(prefix)
    if cur_date > date:
        return False
    return True
