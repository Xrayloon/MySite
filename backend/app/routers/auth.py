from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_ 

from ..core.security import settings, get_password_hash, verify_password, create_access_token, verify_access_token, oauth2_scheme
from ..models import UserCreate, UserFromDB, UserLogin, Token
from ..db.models import UserId
from ..db.database import get_async_session

router = APIRouter(tags=['auth'])

@router.post('/auth/reg', status_code=201)
async def create_user(
    data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = select(UserId).where(
        or_( 
        (func.lower(UserId.username) == data.username.lower()),
        (func.lower(UserId.email) == data.email.lower())
        )
    )
    result = await db.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(400, "Логин и email уже существуют")

    user = UserId(username= data.username,
                  email= data.email.lower(),
                  hashed_password= get_password_hash(data.password)
                )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'id': user.id, 'username':user.username, 'email': user.email}

@router.post("/token", response_model=Token) # Референс https://github.com/CoreyMSchafer/FastAPI-10-Authentication/blob/main/routers/users.py
async def login_for_access_token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    result = await db.execute(
        select(UserId).where( 
            or_(
            func.lower(UserId.email) == data.username.lower(),
            func.lower(UserId.username) == data.username.lower() # По спецификации OAuth2, поле формы должно называться именно username — использовать email вместо него не получится.
            ) 
        )
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email/username или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(UserId.id)},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, Token_type="bearer")

    
