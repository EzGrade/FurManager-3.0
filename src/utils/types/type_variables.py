from typing import TypeVar

from core.models.base import BaseEntityModel
from core.orm.filters.base import BaseFilterModel
from core.orm.models.base import BaseOrmModel
from core.orm.sorters.base import BaseSortModel

BaseEntityModelT = TypeVar("BaseEntityModelT", bound=BaseEntityModel)

ORMModelT = TypeVar("ORMModelT", bound=BaseOrmModel, contravariant=True)

FilterModelT = TypeVar("FilterModelT", bound=BaseFilterModel)
SortModelT = TypeVar("SortModelT", bound=BaseSortModel, contravariant=True)

CreateModelT = TypeVar("CreateModelT", bound=BaseEntityModel, contravariant=True)
UpdateModelT = TypeVar("UpdateModelT", bound=BaseEntityModel, contravariant=True)
