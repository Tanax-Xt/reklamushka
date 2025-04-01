"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

import uuid

from src.api.clients.models import Client
from src.api.clients.schemas import ClientSchema
from src.db.deps import Session


def get_client_by_id(clientId: uuid.UUID, session: Session) -> Client:
    return session.query(Client).filter(Client.id == clientId).first()


def update_client(client_schema: ClientSchema, session: Session) -> None:
    client = session.query(Client).filter(Client.id == client_schema.client_id).first()
    if client is None:
        client = Client(
            id=client_schema.client_id,
            login=client_schema.login,
            age=client_schema.age,
            location=client_schema.location,
            gender=client_schema.gender,
        )
        session.add(client)
    else:
        client.login = client_schema.login
        client.age = client_schema.age
        client.location = client_schema.location
        client.gender = client_schema.gender

    session.commit()


def client_to_schema(client: Client) -> ClientSchema:
    return ClientSchema(
        client_id=client.id,
        login=client.login,
        age=client.age,
        location=client.location,
        gender=client.gender,
    )
