from dataclasses import dataclass
from typing import ClassVar, Type, Any, Union

from sqlalchemy import insert, select, exists, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.dto import BaseModelDTO
from core.interfaces.repository import RepositoryInterface, IDType
from core.interfaces.specification import OnConflictInterface, SpecificationInterface
from infrastructure.db.base import Base
from infrastructure.db.exceptions import raise_from_pg_error, DoesNotExists
from infrastructure.db.utils import safe_and_, get_conditions, safe_or_


@dataclass
class OnConflictUpdate(OnConflictInterface):
    update_data: dict
    index_elements: list[str]

    def apply_conflict(self, insert_query):
        return insert_query.on_conflict_do_update(
            index_elements=self.index_elements,
            set_=self.update_data
        )


class SQLAlchemyRepository(RepositoryInterface):
    # dependency
    session: AsyncSession

    # attrs
    model: ClassVar[Type[Base]]
    base_filters: ClassVar[dict[str, Any] | None] = None

    def _get_returning_fields(
        self,
        returning_dto: Type[BaseModelDTO] | None,
        excluded_fields: set | None,
        specifications: list[SpecificationInterface] | None
    ):
        if returning_dto is None:
            fields = [self.model.id]
        else:
            fields = [
                getattr(self.model, field)
                for field in returning_dto.model_fields.keys()
                if (not excluded_fields or field not in excluded_fields) and hasattr(self.model, field)
            ]
        for spec in specifications or []:
            fields = spec.apply_fields(fields)
        return fields

    def _update_base_filters(
        self,
        filters: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        if self.base_filters is not None:
            filters = {**self.base_filters, **filters}
        return filters

    def _apply_specifications(
        self,
        query,
        specifications: list[SpecificationInterface] | None
    ):
        for spec in specifications or []:
            query = spec.apply(query)
        return query

    async def _execute_query(
        self,
        query,
        returning_dto: Type[BaseModelDTO] | None,
        many: bool = False,
    ) -> IDType | Type[BaseModelDTO] | list[IDType | Type[BaseModelDTO]]:
        try:
            cursor = await self.session.execute(query)
        except IntegrityError as exc:
            raise_from_pg_error(exc)
        mappings = cursor.mappings()
        if many:
            rows = mappings.all()
            if returning_dto is None:
                return [r['id'] for r in rows]
            return [
                returning_dto.model_validate(r, from_attributes=True)
                for r in rows
            ]
        else:
            row = mappings.first()
            if not row:
                where_clause = query.whereclause
                if where_clause is not None:
                    try:
                        compiled_where = where_clause.compile(
                            compile_kwargs={"literal_binds": True}
                        )
                        filters_info = str(compiled_where)
                    except Exception:
                        # Fallback для типов, которые не поддерживают literal_binds (UUID, JSON и т.д.)
                        filters_info = str(where_clause)
                else:
                    filters_info = "No WHERE conditions"

                raise DoesNotExists(
                    f'{self.model.__name__} not found with filters: '
                    f'{filters_info}'
                )
            if returning_dto is None:
                return row['id']
            return returning_dto.model_validate(row, from_attributes=True)

    def incr_field(self, field: str, count: int | float):
        return getattr(self.model, field) + count

    def decr_field(self, field: str, count: int | float):
        return getattr(self.model, field) - count

    async def fetch(
        self,
        returning_dto: Type[BaseModelDTO] | None = None,
        excluded_fields: set | None = None,
        specifications: list[SpecificationInterface] | None = None,
        conditions_method: str = 'and',
        **filters
    ) -> IDType | BaseModelDTO:
        fields = self._get_returning_fields(
            returning_dto, excluded_fields, specifications
        )
        filters = self._update_base_filters(filters)
        if conditions_method == 'and':
            conditions = safe_and_(*get_conditions(self.model, **filters))
        elif conditions_method == 'or':
            conditions = safe_or_(*get_conditions(self.model, **filters))
        else:
            raise TypeError('Conditions method must be one of and / or.')
        q = (
            select(*fields)
            .where(conditions)
        )
        q = self._apply_specifications(q, specifications)
        return await self._execute_query(q, returning_dto, many=False)

    async def fetch_many(
        self,
        returning_dto: Type[BaseModelDTO] | None = None,
        excluded_fields: set | None = None,
        specifications: list[SpecificationInterface] | None = None,
        **filters
    ) -> list[Union[IDType | BaseModelDTO]]:
        fields = self._get_returning_fields(
            returning_dto, excluded_fields, specifications
        )
        filters = self._update_base_filters(filters)
        q = (
            select(*fields)
            .where(safe_and_(*get_conditions(self.model, **filters)))
        )
        q = self._apply_specifications(q, specifications)
        return await self._execute_query(q, returning_dto, many=True)

    async def check(
        self,
        specifications: list[SpecificationInterface] | None = None,
        **filters
    ) -> bool:
        filters = self._update_base_filters(filters)
        q = (
            exists(self.model)
            .where(safe_and_(*get_conditions(self.model, **filters)))
            .select()
        )
        q = self._apply_specifications(q, specifications)
        cursor = await self.session.execute(q)
        return bool(cursor.scalar())

    async def update(
        self,
        update_data: dict,
        returning_dto: Type[BaseModelDTO] | None = None,
        excluded_fields: set | None = None,
        specifications: list[SpecificationInterface] | None = None,
        **filters
    ) -> IDType | BaseModelDTO:
        fields = self._get_returning_fields(
            returning_dto, excluded_fields, specifications
        )
        filters = self._update_base_filters(filters)
        q = (
            update(self.model)
            .where(safe_and_(*get_conditions(self.model, **filters)))
            .values(update_data)
            .returning(*fields)
        )
        q = self._apply_specifications(q, specifications)
        return await self._execute_query(q, returning_dto, many=False)

    async def update_many(
        self,
        update_data: dict,
        returning_dto: Type[BaseModelDTO] | None = None,
        excluded_fields: set | None = None,
        specifications: list[SpecificationInterface] | None = None,
        **filters
    ) -> list[Union[IDType, BaseModelDTO]]:
        fields = self._get_returning_fields(
            returning_dto, excluded_fields, specifications
        )
        filters = self._update_base_filters(filters)
        q = (
            update(self.model)
            .where(safe_and_(*get_conditions(self.model, **filters)))
            .values(update_data)
            .returning(*fields)
        )
        q = self._apply_specifications(q, specifications)
        return await self._execute_query(q, returning_dto, many=True)

    async def create(
        self,
        create_data: BaseModelDTO | dict,
        returning_dto: Type[BaseModelDTO] | None = None,
        excluded_fields: set | None = None,
        specifications: list[SpecificationInterface] | None = None,
        on_conflict: OnConflictInterface | None = None,
    ) -> IDType | BaseModelDTO:
        fields = self._get_returning_fields(
            returning_dto, excluded_fields, specifications
        )
        create_data = create_data if isinstance(create_data, dict) else create_data.model_dump()
        insert_query = insert(self.model)
        if on_conflict:
            insert_query = on_conflict.apply_conflict(pg_insert(self.model))
        q = (
            insert_query
            .values(**create_data)
            .returning(*fields)
        )
        q = self._apply_specifications(q, specifications)
        return await self._execute_query(q, returning_dto, many=False)
