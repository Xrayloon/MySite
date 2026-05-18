from uuid import uuid4, UUID
from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    ForeignKey,
    Text,
    Numeric,
    Uuid,
)
from sqlalchemy.orm import(
    Mapped,
    mapped_column,
    relationship,
)

from .database import Base

class User(Base): # Данные для авторизации 
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4) 
    username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False, index= True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    hashed_password: Mapped[str]  = mapped_column(String, nullable=False) # хэшированный пароль

    profile: Mapped["UserInfo"] = relationship(back_populates="user")
 

class UserInfo(Base): # личный кабинет c доп информации для автозаполнения
    __tablename__ =  'userinfo'

    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    second_name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True, unique=True) 
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("user.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates='profile')

class Tokens(Base):
    __tablename__ = 'tokens'

    access_token: Mapped[str] = mapped_column(String(500),nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("user.id"), primary_key=True)


class Item(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False, index=True)
    price: Mapped[int] = mapped_column(Numeric(10,2), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(25),nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    

"""
class Cart(Base):
    __tablename__ = 'cart'

    id_item: Mapped[int] = mapped_column()
    name_item: Mapped[int]
    count: Mapped[int]
    price_item: Mapped[int] = mapped_column(Numeric(10,2),nullable=False)

    
    """

