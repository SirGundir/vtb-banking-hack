from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.banks.schemas import BankSchema
from api.v1.depends.auth import token_user_dep, user_dep
from api.v1.depends.cqrs import CommandDependency, QueryDependency
from api.v1.schemas import OkResponseSchema
from application.banks.dto import AddBankDTO
from application.banks.services import BankService, ConnectBankService

router = APIRouter(prefix='/banks')


bank_command_dep = Annotated[BankService, Depends(CommandDependency(BankService))]
bank_query_dep = Annotated[BankService, Depends(QueryDependency(BankService))]
connect_command_dep = Annotated[ConnectBankService, Depends(CommandDependency(ConnectBankService))]


@router.get('/', response_model=list[BankSchema], tags=['bank'])
async def get_banks(
    user: token_user_dep,
    bank_service: bank_query_dep,
):
    return await bank_service.get_banks()


@router.post('/', response_model=BankSchema, tags=['bank'])
async def add_bank(
    bank_data: AddBankDTO,
    # ToDo admin only user: token_user_dep,
    bank_service: bank_command_dep,
):
    return await bank_service.add_bank(bank_data)


@router.post('/{bankId}/add-consent/', response_model=OkResponseSchema, tags=['bank'])
async def connect_user_bank(
    user: user_dep,
    bank_service: connect_command_dep,
    bankId: int
):
    await bank_service.connect_user_bank(bankId, user)
    return OkResponseSchema()