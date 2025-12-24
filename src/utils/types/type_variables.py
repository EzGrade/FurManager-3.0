from typing import TypeVar

from src.core.models.base import BaseEntityModel
from src.core.orm.filters.base import BaseFilterModel
from src.core.orm.models.base import BaseOrmModel
from src.core.orm.schemas.base import BaseModelSchema
from src.core.orm.sorters.base import BaseSortModel

BaseEntityModelT = TypeVar("BaseEntityModelT", bound=BaseEntityModel)

ORMModelT = TypeVar("ORMModelT", bound=BaseOrmModel, contravariant=True)

FilterModelT = TypeVar("FilterModelT", bound=BaseFilterModel)
SortModelT = TypeVar("SortModelT", bound=BaseSortModel, contravariant=True)

CreateModelT = TypeVar("CreateModelT", bound=BaseModelSchema, contravariant=True)
UpdateModelT = TypeVar("UpdateModelT", bound=BaseModelSchema, contravariant=True)
