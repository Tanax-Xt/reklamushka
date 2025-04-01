"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from fastapi import APIRouter, HTTPException, status

from src.api.clients.schemas import ClientSchema
from src.api.clients.services import client_to_schema, get_client_by_id, update_client
from src.db.deps import Session

client_router = APIRouter(prefix="/clients", tags=["Clients"])


@client_router.get(
    "/{clientId}",
    status_code=status.HTTP_200_OK,
    response_description="Информация о клиенте успешно получена.",
    response_model=ClientSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Client not found",
        },
    },
)
async def get_client(clientId: uuid.UUID, session: Session = Session):
    client = get_client_by_id(clientId, session)

    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    return client_to_schema(client)


@client_router.post(
    "/bulk",
    status_code=status.HTTP_200_OK,
    response_description="Успешное создание/обновление клиентов",
    response_model=list[ClientSchema],
)
async def bulk_clients(clients_list: list[ClientSchema], session: Session = Session):
    for client in clients_list:
        update_client(client, session)
    return clients_list
