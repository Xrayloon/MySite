import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine,Table,MetaData, Column, Integer, String, Text, ForeignKey

DATABASE_URL = "postgresql+psycopg2://postgres:1@localhost/apishops"

engine = create_engine(DATABASE_URL, echo=True, future=True) # Перед релизом убрать echo и future

connetction = psycopg2.connect(user="postgres", password='1')
connetction.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


