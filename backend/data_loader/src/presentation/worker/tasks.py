from pydantic import BaseModel


class User(BaseModel):
    user_id: int


async def download_accounts(user_id: int):
    print(f">>>{user_id=}")
    return user_id


async def download_account_transactions():
    pass
