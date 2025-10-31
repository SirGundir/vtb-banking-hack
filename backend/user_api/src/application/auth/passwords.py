import random
import re
import string

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from application.auth.exceptions import PasswordValidationError

PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{6,}$')


def hash_password(password: str, secret_key: str) -> str:
    return pbkdf2_sha256.using(salt=secret_key.encode()).hash(password)


def verify_password(plain_password: str, hashed_password: str | None):
    if not hashed_password:
        return False
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def validate_password(password):
    if not PASSWORD_PATTERN.match(password):
        raise PasswordValidationError()


def generate_password(length=8, use_special_chars=True):
    """
    Generates a random secure password of specified length.

    Parameters:
    - length (int): Length of the password (minimum 4). Default is 12.
    - use_special_chars (bool): Whether to include special characters. Default is True.

    Returns:
    - str: The generated password.

    Raises:
    - ValueError: If the specified length is less than 4.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    chars = string.ascii_letters + string.digits
    if use_special_chars:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/"

    # Ensure at least one character from each required set
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
    ]
    if use_special_chars:
        password.append(random.choice("!@#$%^&*()-_=+[]{}|;:,.<>?/"))

    # Fill the rest of the password
    while len(password) < length:
        password.append(random.choice(chars))

    random.shuffle(password)
    return ''.join(password)

