import base64
import hashlib
import hmac
import time
from dataclasses import dataclass
from uuid import UUID

from jwt.utils import force_bytes
from pydantic import UUID4

from application.auth.dto import UserDTO
from infrastructure.config.app import AppConfig
from utils.converters import int_to_base36, base36_to_int


@dataclass
class UserCrypto:
    config: AppConfig
    salt_key = 'auth.services.UserCrypto'
    user_token_sep = '-'

    @staticmethod
    def decode_uidb64(uidb64: str) -> UUID4:
        decoded = base64.b64decode(uidb64).decode()
        return UUID(decoded)

    @staticmethod
    def encode_uidb64(user_id: UUID4) -> str:
        return base64.b64encode(force_bytes(str(user_id))).decode()

    def make_user_token_with_ts(
        self,
        user: UserDTO,
        ts: int,
    ) -> str:
        salt = self.config.secret_key
        ts_b36 = int_to_base36(ts)
        hash_value = force_bytes(f"{str(user.id)}{user.password}{user.email}{ts_b36}")
        salt = force_bytes(self.salt_key + salt)
        salted_hmac = hashlib.pbkdf2_hmac(
            'sha256', hash_value, salt, 10000)
        sign = hmac.new(
            force_bytes(salt),
            salted_hmac,
            hashlib.sha256
        ).hexdigest()[::2]  # Limit to shorten the URL.
        return f"{ts_b36}{self.user_token_sep}{sign.replace(self.user_token_sep, '')}"

    @classmethod
    def verify_user_token(cls, user: UserDTO, token: str) -> bool:
        ts_b36, _ = token.split(cls.user_token_sep)

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if int(time.time()) > ts:
            return False

        if token != cls.make_user_token_with_ts(user, ts):
            return False

        return True
