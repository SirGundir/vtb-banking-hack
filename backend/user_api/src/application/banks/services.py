import json
import random
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass

from faststream.kafka import KafkaBroker

from application.auth.dto import UserDTO
from application.banks.dto import BankDTO, AddBankDTO

from core.exceptions import ActionNotAllowedError
from infrastructure.clients import BankOpenApiInterface, ConsentRequest
from infrastructure.config.app import AppConfig
from infrastructure.db.exceptions import AlreadyExistsError
from infrastructure.db.models.users import ConsentData
from infrastructure.repositories.banks import BankRepository
from infrastructure.repositories.users import UserRepository, update_consents, delete_consent
from log import get_logger


logger = get_logger(__name__)


DOWNLOAD_USER_ACCOUNT_TOPIC = 'download_user_account'
DOWNLOAD_BANK_PRODUCTS_TOPIC = 'download_bank_products'
DOWNLOAD_BANK_PRODUCT_DETAILS_TOPIC = 'download_bank_product_details'


@dataclass
class BankService:
    user_repository: UserRepository
    bank_repository: BankRepository
    bank_api: BankOpenApiInterface
    broker: KafkaBroker

    config: AppConfig

    async def add_bank(self, bank: AddBankDTO):
        access_data = await self.bank_api.with_api_url(bank.api_url).get_bank_token(
            bank.client_id, bank.client_secret
        )
        create_data = bank.model_dump()
        access_data['timestamp'] = time.time()
        create_data['access_data'] = access_data
        bank = await self.bank_repository.create(create_data, returning_dto=BankDTO)
        async with self.broker as br:
            await br.publish(bank.id, DOWNLOAD_BANK_PRODUCTS_TOPIC)
        return bank

    async def get_banks(self) -> list[BankDTO]:
        return await self.bank_repository.fetch_many(returning_dto=BankDTO, is_active=True)

    async def get_bank(self, bank_id: int, update_access: bool = False) -> BankDTO:
        bank: BankDTO = await self.bank_repository.fetch(returning_dto=BankDTO, id=bank_id)
        if update_access and bank.access_expired:
            access_data = await self.bank_api.with_api_url(bank.api_url).get_bank_token(
                bank.client_id, bank.client_secret
            )
            access_data['timestamp'] = time.time()
            bank = await self.bank_repository.update(dict(access_data=access_data), returning_dto=BankDTO)
        return bank


@dataclass
class ConnectBankService:
    user_repository: UserRepository
    bank_service: BankService
    bank_api: BankOpenApiInterface
    broker: KafkaBroker

    async def connect_user_bank(self, bank_id: int, user: UserDTO):
        if user.consents and bank_id in user.consents:
            raise AlreadyExistsError(f"Bank {bank_id} already connected to user")

        bank: BankDTO = await self.bank_service.get_bank(bank_id, update_access=True)
        bank_client_id = f"team221-1"
        consent_id = await self.bank_api.with_api_url(bank.api_url).create_consent(ConsentRequest(
            bank_client_id=bank_client_id,
            client_id=bank.client_id,
            client_secret=bank.client_secret,
            access_token=bank.access_token
        ))
        update_data = dict(
            consents=update_consents(bank_id, ConsentData(
                bank_client_id=bank_client_id,
                consent_id=consent_id,
            ))
        )
        await self.user_repository.update(update_data, id=user.id)
        logger.info(f"Connected bank {bank_id} to user {user.id}")
        async with self.broker as br:
            res = await br.publish(dict(user_id=str(user.id), bank_id=bank_id), DOWNLOAD_USER_ACCOUNT_TOPIC)
        print(f">>>{consent_id=}, {bank_client_id=}, {res=}")
        logger.info(f"Schedule downloading user data for user {user.id}")

    async def reject_user_consent(self, bank_id: int, user: UserDTO):
        if user.consents and bank_id not in user.consents:
            raise ActionNotAllowedError(f"Bank {bank_id} not connected to user")

        bank: BankDTO = await self.bank_service.get_bank(bank_id)
        await self.bank_api.with_api_url(bank.api_url).delete_consent(
            user.consents[bank_id].consent_id
        )
        update_data = dict(
            consents=delete_consent(bank_id)
        )
        await self.user_repository.update(update_data, id=user.id)
        logger.info(f"Disconnected bank {bank_id} to user {user.id}")

