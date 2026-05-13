from datetime import datetime, timedelta, timezone,UTC
import jwt
from typing import Any
from fastapi.security import OAuth2PasswordBearer

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/user/token')


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt

def verify_access_token(token: str) -> str | None:

    try:
        playload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"require": {"exp", "sub"}},
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return playload.get("sub")
    

def verify_password(
        plain_password: str, hashed_password: str # 1 веденный пароль,2й хеш из бд
) -> tuple[bool, str | None]: # в True или False и хеш пароль или нечего
    return password_hash.verify_and_update(plain_password, hashed_password) 


def get_password_hash(password: str) -> str:
    return password_hash.hash(password) # создает и сохраняет новый хеш