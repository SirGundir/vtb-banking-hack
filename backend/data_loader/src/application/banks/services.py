from dataclasses import dataclass

from application.user_accounts.dto import BankDTO
from infrastructure.data_loaders.bank import BankProductsLoader
from infrastructure.repositories.banks import BankRepository


@dataclass
class BankProductService:
    bank_repository: BankRepository
    loader: BankProductsLoader

    async def download_products(self, bank_id: int):
        bank: BankDTO = await self.bank_repository.fetch(returning_dto=BankDTO, id=bank_id)
        return await self.loader.with_api_url(bank.api_url).get_products(bank.id)
