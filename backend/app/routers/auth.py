from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.security import get_password_hash, verify_password
from ..models import UserCreate, UserFromDB
from ..db.models import UserId
from ..db.database import get_async_session

router = APIRouter(tags=['auth'])

@router.post('/auth/register', status_code=201)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_async_session)):
    statement = select(UserId).where((UserId.username == data.username) | (UserId.email == data.email))
    result = await db.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(400, "Пользователь уже существует")

    user = UserId(username= data.username, email= data.email, hashed_password= get_password_hash(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'id': user.id, 'username':user.username, 'email': user.email}