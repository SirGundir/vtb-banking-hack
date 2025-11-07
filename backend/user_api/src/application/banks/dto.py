import time

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

    @property
    def access_expired(self):
        return time.time() - self.access_data['timestamp'] > self.access_data['expires_in']


class AddBankDTO(BaseModelDTO):
    name: str
    api_url: str = Field(validation_alias='apiUrl')
    client_id: str = Field(validation_alias='clientId')
    client_secret: str = Field(validation_alias='clientSecret')

