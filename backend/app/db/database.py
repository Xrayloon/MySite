from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from backend.app.core.security import settings 

DATABASE_URL = settings.ASYNC_DATABASE_URL

engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
