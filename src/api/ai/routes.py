"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from fastapi import APIRouter, status

from src.ai.generate_text import send_generate_text_response
from src.api.ai.schemas import GeneratedTextSchema, ModerationStateSchema, TextGeneratingRequest
from src.moderation import set_moderation_state

ai_router = APIRouter(prefix="/ai", tags=["Artificial intelligence"])


@ai_router.post(
    "/moderation-campaigns",
    status_code=status.HTTP_200_OK,
    response_description="Состояние модерации рекламных кампаний успешно обновлено.",
    response_model=ModerationStateSchema,
)
async def toggle_ai_moderation(moderation_state_schema: ModerationStateSchema):
    set_moderation_state(int(moderation_state_schema.current_state))
    return moderation_state_schema


@ai_router.post(
    "/generate-text",
    status_code=status.HTTP_200_OK,
    response_description="Рекламный текст сгенерирован.",
    response_model=GeneratedTextSchema,
)
async def generate_text(generation_request: TextGeneratingRequest):
    data = send_generate_text_response(
        generation_request.product,
        generation_request.advertiser_name,
        generation_request.audience,
        generation_request.target,
    )
    return GeneratedTextSchema(title=data["title"], text=data["text"])
