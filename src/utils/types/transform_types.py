from typing import Callable, Sequence

from src.core.orm.schemas.base import ManyResponseSchema
from src.core.models.base import ManyCustomResponse
from src.core.orm.models import ChannelModelORM
from src.core.orm.schemas.channel import ChannelResponseSchema

ChannelTransformOneCallback = Callable[[ChannelModelORM], ChannelResponseSchema]
ChannelListTransformCallback = Callable[
    [ManyCustomResponse[ChannelModelORM]], ManyResponseSchema[ChannelResponseSchema]
]
ChannelTransformAllCallback = Callable[
    [Sequence[ChannelModelORM] | list[ChannelModelORM]],
    list[ChannelResponseSchema],
]
