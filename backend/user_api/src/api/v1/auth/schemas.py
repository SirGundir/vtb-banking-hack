from pydantic import BaseModel, Field, model_validator, field_validator


class JwtTokensSchema(BaseModel):
    access_token: str = Field(serialization_alias='accessToken')
    refresh_token: str = Field(serialization_alias='refreshToken')


class RefreshTokensSchema(BaseModel):
    access_token: str = Field(serialization_alias='newAccessToken')
    refresh_token: str = Field(serialization_alias='newRefreshToken')


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str = Field(validation_alias='refreshToken')

