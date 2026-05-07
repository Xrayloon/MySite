from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from .config import settings

password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


ALGORITHM = 'HS256'

def create_access_token():
    pass

def verify_password(
        plain_password: str, hashed_password: str # 1 веденный пароль,2й хеш из бд
) -> tuple[bool, str | None]: # в True или False и хеш пароль или нечего
    return password_hash.verify_and_update(plain_password, hashed_password) 


def get_password_hash(password: str) -> str:
    return password_hash.hash(password) # создает и сохраняет новый хеш