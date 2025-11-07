from faststream import Depends, Context
from faststream.kafka import KafkaBroker
from pydantic import BaseModel, UUID4

from application.user_accounts.services import UserAccountService
from core.mapers import dto_to_ndjson
from log import get_logger
from presentation.worker.depends.cqrs import CommandDependency
from presentation.worker.topics import CLICKHOUSE_USER_ACCOUNT_TOPIC, DOWNLOAD_USER_BALANCE_TOPIC, \
    CLICKHOUSE_USER_BALANCES_TOPIC

logger = get_logger(__name__)


async def download_accounts(
    user_id: UUID4,
    bank_id: int,
    user_account_service: UserAccountService = Depends(CommandDependency(UserAccountService)),
    broker: KafkaBroker = Context()
):
    try:
        accounts = await user_account_service.download_accounts(user_id, bank_id)
        await broker.publish(dto_to_ndjson(accounts).encode("utf-8"), CLICKHOUSE_USER_ACCOUNT_TOPIC)
        logger.info(f"Publish {len(accounts)}, {user_id=}, {bank_id=}")
        balance_publisher = broker.publisher(DOWNLOAD_USER_BALANCE_TOPIC, batch=True)
        await balance_publisher.publish(*[
            dict(user_id=user_id, bank_id=bank_id, account_id=account.account_id) for account in
            accounts
        ])
    except Exception as exc:
        logger.exception(exc)


async def download_account_balance(
    user_id: UUID4,
    bank_id: int,
    account_id: str,
    user_account_service: UserAccountService = Depends(CommandDependency(UserAccountService)),
    broker: KafkaBroker = Context()
):
    try:
        balances = await user_account_service.download_balance(
            user_id=user_id,
            bank_id=bank_id,
            account_id=account_id
        )
        print(f">>{dto_to_ndjson(balances)=}")
        await broker.publish(dto_to_ndjson(balances).encode("utf-8"), CLICKHOUSE_USER_BALANCES_TOPIC)
        logger.info(f"Publish {len(balances)}, {user_id=}, {bank_id=}, {account_id=}")
    except Exception as exc:
        logger.exception(exc)


async def download_account_transactions():
    pass
