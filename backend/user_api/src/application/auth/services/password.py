from dataclasses import dataclass

from application.auth import messages
from application.auth.crypto import UserCrypto
from application.auth.dto import UserDTO, ChangePasswordDTO, ResetPasswordDTO, SetPasswordDTO
from application.auth.passwords import verify_password, hash_password
from core.exceptions import ValidateDataError
from infrastructure.config.app import AppConfig
from infrastructure.db.exceptions import DoesNotExists
from infrastructure.repositories.users import UserRepository


@dataclass
class PasswordService:
    user_repository: UserRepository
    config: AppConfig

    async def change_password(
        self,
        user: UserDTO,
        passwords: ChangePasswordDTO
    ) -> None:
        if not user.is_email_valid:
            raise ValidateDataError(
                detail=messages.NOT_VERIFIED_EMAIL
            )

        if not user.has_password:
            raise ValidateDataError('Set password before.')

        if not verify_password(passwords.current_password, user.password):
            raise ValidateDataError('Wrong password.')

        update_data = dict(password=hash_password(passwords.new_password, self.config.secret_key))
        await self.user_repository.update(update_data, id=user.id)
        # ToDo send email

    async def request_reset_password(
        self,
        reset_data: ResetPasswordDTO
    ) -> None:
        try:
            user = await self.user_repository.fetch(
                UserDTO, email=reset_data.email
            )
        except DoesNotExists as exc:
            raise ValidateDataError(
                detail=f'User with email {reset_data.email} not found.'
            ) from exc

        if not user.is_email_valid:
            raise ValidateDataError(
                detail=messages.NOT_VERIFIED_EMAIL
            )
        # ToDo send email

    async def reset_password(
        self,
        uidb64: str,
        token: str,
        password_data: SetPasswordDTO
    ) -> None:
        user_id = UserCrypto(self.config).decode_uidb64(uidb64)
        try:
            user = await self.user_repository.fetch(UserDTO, id=user_id)
        except DoesNotExists:
            raise ValidateDataError(messages.PASSWORD_VERIFICATION_ERROR)

        if not UserCrypto.verify_user_token(user, token):
            raise ValidateDataError(messages.PASSWORD_VERIFICATION_ERROR)

        update_data = dict(password=hash_password(password_data.password, self.config.secret_key))
        await self.user_repository.update(update_data, id=user.id)
        # ToDo send email