import random
from dataclasses import dataclass

from faststream.kafka import KafkaBroker

from application.auth.dto import UserDTO
from application.banks.dto import BankDTO, AddBankDTO
from infrastructure.clients import BankOpenApiInterface, ConsentRequest
from infrastructure.config.app import AppConfig
from infrastructure.db.exceptions import AlreadyExistsError
from infrastructure.db.models.users import ConsentData
from infrastructure.repositories.banks import BankRepository
from infrastructure.repositories.users import UserRepository, update_consents
from log import get_logger


logger = get_logger(__name__)


DOWNLOAD_USER_ACCOUNT_TOPIC = 'download_user_account'


@dataclass
class BankService:
    user_repository: UserRepository
    bank_repository: BankRepository
    bank_api: BankOpenApiInterface
    config: AppConfig

    async def add_bank(self, bank: AddBankDTO):
        access_data = await self.bank_api.with_api_url(bank.api_url).get_bank_token(
            bank.client_id, bank.client_secret
        )
        create_data = bank.model_dump()
        create_data['access_data'] = access_data
        bank = await self.bank_repository.create(create_data, returning_dto=BankDTO)
        return bank

    async def get_banks(self) -> list[BankDTO]:
        return await self.bank_repository.fetch_many(returning_dto=BankDTO, is_active=True)



@dataclass
class ConnectBankService:
    user_repository: UserRepository
    bank_repository: BankRepository
    bank_api: BankOpenApiInterface
    broker: KafkaBroker

    async def connect_user_bank(self, bank_id: int, user: UserDTO):
        if user.consents and bank_id in user.consents:
            raise AlreadyExistsError(f"Bank {bank_id} already connected to user")

        bank: BankDTO = await self.bank_repository.fetch(returning_dto=BankDTO, id=bank_id)
        bank_client_id = f"team221-{random.randint(1, 5)}"
        consent_id = await self.bank_api.with_api_url(bank.api_url).create_consent(ConsentRequest(
            bank_client_id=bank_client_id,
            client_id=bank.client_id,
            client_secret=bank.client_secret,
            access_token=bank.access_token
        ))
        update_data = dict(
            consents=update_consents(bank_id, ConsentData(
                bank_client_id=bank_client_id,
                consent_id=consent_id
            ))
        )
        await self.user_repository.update(update_data, id=user.id)
        logger.info(f"Connected bank {bank_id} to user {user.id}")
        publisher = self.broker.publisher(DOWNLOAD_USER_ACCOUNT_TOPIC)
        await publisher.publish(str(user.id))
        logger.info(f"Schedule downloading user data for user {user.id}")
