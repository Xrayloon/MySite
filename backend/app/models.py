from sqlalchemy import Table,MetaData, Column, Integer, String, ForeignKey
#TO-DO: переместить сюда все модели таблицы и дополнять их 

user_info = Table(
    'user_info', MetaData,
    Column('id', Integer(), primary_key=True),
    Column('nickname', String(200), nullable=False),
    Column('email',String(150), unique=True, nullable=False)
)

user_profile = Table(
    'user_profile', MetaData,
    Column('first_name', String(50), nullable=True),
    Column('second_name',String(50), nullable=True),
    Column('phone_nubmer',String(20), nullable=True, unique=True),
    Column('user_id', ForeignKey('user_info.id')),
)

