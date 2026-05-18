import uuid
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..core.security import settings, get_password_hash, verify_password, create_access_token, verify_access_token, oauth2_scheme
from ..models import UserCreate, UserPrivate, UserUpdate, Token
from ..db.models import User, Tokens, UserInfo
from ..db.database import get_async_session

router = APIRouter(tags=['user'])

@router.post('/reg', status_code=201)
async def create_user(
    data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await db.execute(
        select(User)
        .where(func.lower(User.username)== data.username.lower()
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username уже зарегистрирован"
        )
    result = await db.execute(
        select(User)
        .where(func.lower(User.email) == data.email.lower()
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
            )

    new_user = User(
        username= data.username,
        email= data.email.lower(),
        hashed_password= get_password_hash(data.password)
        )
    db.add(new_user)
    
    await db.commit()
    await db.refresh(new_user)
    return {'id': new_user.id, 'username':new_user.username, 'email': new_user.email}

@router.patch('/{user_id}')
async def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)]
    ):
    # Поиск пользователя
    result = await db.execute(
        select(User, UserInfo)
        .outerjoin(UserInfo, User.id == UserInfo.user_id)
        .where(User.id == user_id)
    )
    row = result.one_or_none()
    if not row:
        # Ошибка - Не найден
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    user, user_info = row
    # Пришел ли номер на проверку? Нет тогда None
    current_phone = user_info.phone_number if user_info else None
    # Проверка уникальности телефона 
    if user_update.phone_number is not None:
        result = await db.execute(
            select(UserInfo.user_id)
            .where(UserInfo.phone_number == user_update.phone_number,
                   UserInfo.user_id != user_id
                   ))
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Данный номер телефона уже используется"
            )
        # Создаем колонку что бы бд знала куда добовлять 
    if user_info is None:
        user_info = UserInfo(user_id=user_id)
        db.add(user_info)

    for field,value in user_update.model_dump(exclude_unset=True).items():
        setattr(user_info, field, value)

    await db.commit()
    await db.refresh(user)

    return {"user": user_info}

@router.post("/token", response_model=Token) # Референс https://github.com/CoreyMSchafer/FastAPI-10-Authentication/blob/main/routers/users.py
async def login_for_access_token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    result = await db.execute(
        select(User).where(  # Вход с username`ма или с почты
            or_(
            func.lower(User.email) == data.username.lower(), # По спецификации OAuth2, поле формы должно называться именно username — использовать email вместо него не получится.
            func.lower(User.username) == data.username.lower() 
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
        data={"sub": str(User.id)},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, Token_type="bearer")
