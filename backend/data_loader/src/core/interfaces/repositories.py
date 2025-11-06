from typing import Protocol, Type

from pydantic import BaseModel, UUID4

from core.interfaces.specification import SpecificationInterface


class RepositoryInterface(Protocol):

    @staticmethod
    def incr_field(field: str, count: int | float):
        raise NotImplementedError

    @staticmethod
    def decr_field(field: str, count: int | float):
        raise NotImplementedError

    async def add(self, **create_data) -> BaseModel:
        raise NotImplementedError

    async def fetch(
        self,
        specifications: list[SpecificationInterface] | None = None,
        **filters
    ) -> BaseModel:
        raise NotImplementedError

    async def fetch_many(
        self,
        specifications: list[SpecificationInterface] | None = None,
        **filters
    ) -> list[BaseModel]:
        raise NotImplementedError

    async def update(
        self,
        update_data: dict,
        returning_dto: Type[BaseModel] | None = None,
        excluded_fields: set | None = None,
        specifications: list[SpecificationInterface] | None = None,
        **filters,
    ) -> BaseModel | None:
        raise NotImplementedError

    async def update_many(
        self,
        update_data: dict,
        returning_dto: Type[BaseModel] | None = None,
        excluded_fields: set | None = None,
        specifications: list[SpecificationInterface] | None = None,
        **filters,
    ) -> list[BaseModel]:
        raise NotImplementedError

    async def check(
        self,
        specifications: list[SpecificationInterface] | None = None,
        **filters
    ) -> bool:
        raise NotImplementedError

    async def remove(
        self,
        id_field: int,
    ) -> int:
        raise NotImplementedError


IDType = UUID4 | int


class UserRepositoryInterface(RepositoryInterface): ...