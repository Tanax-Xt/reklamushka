"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from typing import Any

from redis import Redis

from src.config import settings

redis = Redis(settings.REDIS_HOST, settings.REDIS_PORT)

CACHE_KEYS_SEPARATOR = ":"


def separate(*args: Any):
    return CACHE_KEYS_SEPARATOR.join(args)


__all__ = [
    "redis",
]
