from typing import Sequence

from src.core.models.base import ManyCustomResponse
from src.core.models.channel_config.entity import (
    ChannelConfigModel,
)
from src.core.orm.models import ChannelConfigModelORM
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.channel_config import (
    ChannelConfigResponseSchema,
    ChannelConfigCreateSchema,
    ChannelConfigUpdateSchema,
)


def transform_orm_channel_config_model_into_response(
        model: ChannelConfigModelORM,
) -> ChannelConfigResponseSchema:
    return ChannelConfigResponseSchema.model_validate(model)


def transform_orm_channel_config_model_into_list_responses(
        models: Sequence[ChannelConfigModelORM] | list[ChannelConfigModelORM],
) -> list[ChannelConfigResponseSchema]:
    return [ChannelConfigResponseSchema.model_validate(model) for model in models]


def transform_orm_channel_config_model_into_many_responses(
        models: ManyCustomResponse[ChannelConfigModelORM],
) -> ManyResponseSchema[ChannelConfigResponseSchema]:
    return ManyResponseSchema(
        count=models.count,
        data=transform_orm_channel_config_model_into_list_responses(models.data),
    )


def transform_channel_config_model_into_update_request(
        model: ChannelConfigModel,
) -> ChannelConfigUpdateSchema:
    return ChannelConfigUpdateSchema(
        uuid=model.uuid,
        is_post_owner_report_enabled=model.is_post_owner_report_enabled,
        updated_at=model.updated_at,
        updated_by_id=model.updated_by,
        channel_id=model.channel,
    )


def transform_channel_config_model_into_create_request(
        model: ChannelConfigModel,
) -> ChannelConfigCreateSchema:
    return ChannelConfigCreateSchema(
        uuid=model.uuid,
        is_post_owner_report_enabled=model.is_post_owner_report_enabled,
        updated_at=model.updated_at,
        updated_by_id=model.updated_by,
        channel_id=model.channel,
    )


def transform_channel_config_model_list_into_create_request(
        models: list[ChannelConfigModel],
) -> list[ChannelConfigCreateSchema]:
    return [transform_channel_config_model_into_create_request(model) for model in models]


def transform_channel_config_model_response_into_channel_config_model(
        model: ChannelConfigResponseSchema,
) -> ChannelConfigModel:
    data = model.model_dump(exclude_unset=True)
    # map DB column names back to domain names
    if "channel_id" in data:
        data["channel"] = data.pop("channel_id")
    if "updated_by_id" in data:
        data["updated_by"] = data.pop("updated_by_id")
    return ChannelConfigModel(**data)


def transform_channel_config_model_into_channel_config_model_response(
        model: ChannelConfigModel,
) -> ChannelConfigResponseSchema:
    data = model.model_dump(exclude_unset=True)
    if "channel" in data:
        data["channel_id"] = data.pop("channel")
    if "updated_by" in data:
        data["updated_by_id"] = data.pop("updated_by")
    return ChannelConfigResponseSchema(**data)


def transform_channel_config_model_response_list_into_channel_config_model(
        models: list[ChannelConfigResponseSchema],
) -> list[ChannelConfigModel]:
    return [
        transform_channel_config_model_response_into_channel_config_model(model) for model in models
    ]
