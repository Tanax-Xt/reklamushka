"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import os

import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.api import api_router
from src.date import date_initialization
from src.db import ENGINE, Base
from src.moderation import moderation_initialization
from src.storage import s3_initialization

Base.metadata.create_all(ENGINE)
date_initialization()
moderation_initialization()
s3_initialization()

app = FastAPI(title="Рекламушка API", version="1.0.0")

Instrumentator().instrument(app).expose(app)

app.include_router(api_router)

if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:8080")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
