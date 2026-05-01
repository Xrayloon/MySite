from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass
