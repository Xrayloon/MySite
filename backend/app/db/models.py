from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import(
    Mapped,
    mapped_column,
)

from .database import Base

class UserId(Base): # Данные для авторизации 
    __tablename__ = "userid"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True) 
    username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    hashed_password: Mapped[str]  = mapped_column(String, nullable=False) # хэшированный пароль

class UserProfile(Base): # личный кабинет c доп информации для автозаполнения
    __tablename__ =  'userinfo'

    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    second_name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True, unique=True) 
    user_id: Mapped[int] = mapped_column(ForeignKey("userid.id"), primary_key=True)

class Item(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
