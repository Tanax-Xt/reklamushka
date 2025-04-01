"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from src.cache import redis
from src.config import settings


def moderation_initialization(prefix=settings.MODERATION_PREFIX):
    if redis.get(prefix) is None:
        set_moderation_state(0, prefix)


def set_moderation_state(state: int, prefix=settings.MODERATION_PREFIX):
    redis.set(prefix, state)


def get_current_moderation_state(prefix=settings.MODERATION_PREFIX):
    return int(redis.get(prefix))
