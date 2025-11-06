from application.auth import messages
from core.exceptions import DetailedError


class AuthorizationError(DetailedError):
    default_message = messages.NOT_AUTHORIZED_MESSAGE


class CredentialsError(DetailedError):
    default_message = messages.NOT_AUTHORIZED_MESSAGE


class ForbiddenError(DetailedError):
    default_message = messages.FORBIDDEN_MESSAGE


class PasswordValidationError(DetailedError):
    default_message = messages.PASSWORD_MESSAGE
