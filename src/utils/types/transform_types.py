from typing import Callable, Sequence

from src.core.models.base import ManyCustomResponse
from src.core.orm.models import ChannelModelORM, UserModelORM, ChannelConfigModelORM
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.channel import ChannelResponseSchema
from src.core.orm.schemas.channel_config import ChannelConfigResponseSchema
from src.core.orm.schemas.user import UserResponseSchema

ChannelTransformOneCallback = Callable[[ChannelModelORM], ChannelResponseSchema]
ChannelListTransformCallback = Callable[
    [ManyCustomResponse[ChannelModelORM]], ManyResponseSchema[ChannelResponseSchema]
]
ChannelTransformAllCallback = Callable[
    [Sequence[ChannelModelORM] | list[ChannelModelORM]],
    list[ChannelResponseSchema],
]

UserTransformOneCallback = Callable[[UserModelORM], UserResponseSchema]
UserListTransformCallback = Callable[
    [ManyCustomResponse[UserModelORM]], ManyResponseSchema[UserResponseSchema]
]
UserTransformAllCallback = Callable[
    [Sequence[UserModelORM] | list[UserModelORM]],
    list[UserResponseSchema],
]

ChannelConfigTransformOneCallback = Callable[[ChannelConfigModelORM], ChannelConfigResponseSchema]
ChannelConfigListTransformCallback = Callable[
    [ManyCustomResponse[ChannelConfigModelORM]], ManyResponseSchema[ChannelConfigResponseSchema]
]
ChannelConfigTransformAllCallback = Callable[
    [Sequence[ChannelConfigModelORM] | list[ChannelConfigModelORM]],
    list[ChannelConfigResponseSchema],
]
