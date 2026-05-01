from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey
)
from sqlalchemy.orm import(
    Mapped,
    mapped_column,
)

from app.db.database import Base

class UserId(Base):
    __tablename__ = "userid"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True) 
    nickname: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

class UserProfile(Base):
    __tablename__ =  'userinfo'

    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    second_name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] =mapped_column(String(20),nullable=True, unique=True) 
    user_id: Mapped[int] = mapped_column(ForeignKey("userid.id"))
    
""" 
user_profile = Table(
    'user_profile', MetaData,
    Column('first_name', String(50), nullable=True),
    Column('second_name',String(50), nullable=True),
    Column('phone_nubmer',String(20), nullable=True, unique=True),
    Column('user_id', ForeignKey('user_info.id')),
)

Старый синтаксис, переделать под 2.0
user_info = Table(
    'user_info', MetaData,
    Column('id', Integer(), primary_key=True),
    Column('nickname', String(200), nullable=False),
    Column('email',String(150), unique=True, nullable=False)
)



"""