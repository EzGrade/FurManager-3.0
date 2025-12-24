from typing import Sequence

from src.core.models.base import ManyCustomResponse
from src.core.models.channel.entity import (
    ChannelModel,
)
from src.core.orm.models import ChannelModelORM
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.channel import (
    ChannelResponseSchema,
    ChannelCreateSchema,
    ChannelUpdateSchema,
)


def transform_orm_channel_model_into_response(
    model: ChannelModelORM,
) -> ChannelResponseSchema:
    return ChannelResponseSchema.model_validate(model)


def transform_orm_channel_model_into_list_responses(
    models: Sequence[ChannelModelORM] | list[ChannelModelORM],
) -> list[ChannelResponseSchema]:
    return [ChannelResponseSchema.model_validate(model) for model in models]


def transform_orm_channel_model_into_many_responses(
    models: ManyCustomResponse[ChannelModelORM],
) -> ManyResponseSchema[ChannelResponseSchema]:
    return ManyResponseSchema(
        count=models.count,
        data=transform_orm_channel_model_into_list_responses(models.data),
    )


def transform_channel_model_into_update_request(
    model: ChannelModel,
) -> ChannelUpdateSchema:
    return ChannelUpdateSchema(
        uuid=model.uuid,
        name=model.name,
        title=model.title,
        telegram_id=model.telegram_id,
        owner_id=model.owner_id,
    )


def transform_channel_model_into_create_request(
    model: ChannelModel,
) -> ChannelCreateSchema:
    return ChannelCreateSchema(
        uuid=model.uuid,
        name=model.name,
        title=model.title,
        telegram_id=model.telegram_id,
        owner_id=model.owner_id,
    )


def transform_channel_model_list_into_create_request(
    models: list[ChannelModel],
) -> list[ChannelCreateSchema]:
    return [transform_channel_model_into_create_request(model) for model in models]


def transform_channel_model_response_into_channel_model(
    model: ChannelResponseSchema,
) -> ChannelModel:
    return ChannelModel(**model.model_dump(exclude_unset=True))


def transform_channel_model_into_channel_model_response(
    model: ChannelModel,
) -> ChannelResponseSchema:
    return ChannelResponseSchema(**model.model_dump(exclude_unset=True))


def transform_channel_model_response_list_into_channel_model(
    models: list[ChannelResponseSchema],
) -> list[ChannelModel]:
    return [
        transform_channel_model_response_into_channel_model(model) for model in models
    ]
