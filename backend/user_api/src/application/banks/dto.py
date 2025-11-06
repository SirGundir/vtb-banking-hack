from pydantic import Field

from core.dto import BaseModelDTO


class BankDTO(BaseModelDTO):
    id: int
    name: str
    client_id: str = Field(exclude=True)
    client_secret: str = Field(exclude=True)
    access_data: dict = Field(exclude=True)
    api_url: str

    @property
    def access_token(self):
        return self.access_data['access_token']


class AddBankDTO(BaseModelDTO):
    name: str
    api_url: str = Field(validation_alias='apiUrl')
    client_id: str = Field(validation_alias='clientId')
    client_secret: str = Field(validation_alias='clientSecret')

