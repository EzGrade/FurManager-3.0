from typing import Sequence

from src.core.models.base import ManyCustomResponse
from src.core.models.user.entity import (
    UserModel,
)
from src.core.orm.models import UserModelORM
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.user import (
    UserResponseSchema,
    UserCreateSchema,
    UserUpdateSchema,
)


def transform_orm_user_model_into_response(
        model: UserModelORM,
) -> UserResponseSchema:
    return UserResponseSchema.model_validate(model)


def transform_orm_user_model_into_list_responses(
        models: Sequence[UserModelORM] | list[UserModelORM],
) -> list[UserResponseSchema]:
    return [UserResponseSchema.model_validate(model) for model in models]


def transform_orm_user_model_into_many_responses(
        models: ManyCustomResponse[UserModelORM],
) -> ManyResponseSchema[UserResponseSchema]:
    return ManyResponseSchema(
        count=models.count,
        data=transform_orm_user_model_into_list_responses(models.data),
    )


def transform_user_model_into_update_request(
        model: UserModel,
) -> UserUpdateSchema:
    return UserUpdateSchema(
        uuid=model.uuid,
        first_name=model.first_name,
        last_name=model.last_name,
        telegram_id=model.telegram_id,
    )


def transform_user_model_into_create_request(
        model: UserModel,
) -> UserCreateSchema:
    return UserCreateSchema(
        uuid=model.uuid,
        first_name=model.first_name,
        last_name=model.last_name,
        username=model.username,
        telegram_id=model.telegram_id,
        joined_at=model.joined_at,
    )


def transform_user_model_list_into_create_request(
        models: list[UserModel],
) -> list[UserCreateSchema]:
    return [transform_user_model_into_create_request(model) for model in models]


def transform_user_model_response_into_user_model(
        model: UserResponseSchema,
) -> UserModel:
    return UserModel(**model.model_dump(exclude_unset=True))


def transform_user_model_into_user_model_response(
        model: UserModel,
) -> UserResponseSchema:
    return UserResponseSchema(**model.model_dump(exclude_unset=True))


def transform_user_model_response_list_into_user_model(
        models: list[UserResponseSchema],
) -> list[UserModel]:
    return [
        transform_user_model_response_into_user_model(model) for model in models
    ]
