from typing import ClassVar

from aiohttp import ClientError

from core.dto import BankProductsDTO
from infrastructure.data_loaders.http import HttpLoader, DownloadError, NOT_SET_URL


class BankProductsLoader(HttpLoader):
    endpoint: ClassVar[str] = 'products'

    async def get_products(self, bank_id: int) -> list[BankProductsDTO]:
        assert self.api_url != NOT_SET_URL
        try:
            response = await self._make_request(self.endpoint)
        except ClientError as exc:
            raise DownloadError(self.endpoint) from exc

        if error := response.get('error'):
            raise DownloadError(self.endpoint, error)

        if not (products := response.get('data', {}).get('product')):
            raise DownloadError(self.endpoint, str(response))
        return [
            BankProductsDTO(bank_id=bank_id, **data) for data in products
        ]

    async def get_product_details(self, bank_id: int, product_id: str) -> list[BankProductsDTO]:
        assert self.api_url != NOT_SET_URL
        try:
            response = await self._make_request(f"{self.endpoint}/{product_id}")
        except ClientError as exc:
            raise DownloadError(self.endpoint) from exc

        if error := response.get('error'):
            raise DownloadError(f"{self.endpoint}/{product_id}", error)

        print(f">>{response=}")

        # if not (products := response.get('data', {}).get('product')):
        #     raise DownloadError(f"{self.endpoint}/{product_id}", str(response))
        # print(products)
        # return [
        #     BankProductsDTO(bank_id=bank_id, **data) for data in products
        # ]
