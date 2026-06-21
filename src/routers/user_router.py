import asyncio
from sqlalchemy import Select, or_
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.database.models import User
from src.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from typing import Annotated, List

from passlib.context import CryptContext

from src.auth.auth import get_current_user
from src.rate_limit.rate_limit import limiter

router = APIRouter(
    tags=["users"]
)

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


async_db = Annotated[AsyncSession, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]


@router.post("/user_create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# @limiter.limit("10/minute")
async def create_user(user: UserCreate, db: async_db, request: Request):
    result = await db.execute(Select(User).where(or_(User.email == user.email, User.name == user.name)))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already exists"
        )
    db_user = User(
        name=user.name, email=user.email, password=bcrypt.hash(user.password)
    )
    db.add(db_user)
    print(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user



@router.put("/user",response_model=UserResponse,status_code=status.HTTP_200_OK)
async def update_user(user_update: UserUpdate, db: async_db, user: user_dependancy):
    result = await db.execute(Select(User).where(User.id == user.get("id")))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_details = user_update.model_dump(exclude_unset=True, exclude_none=True)
    print(user_details)
    for key, value in user_details.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/user/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: async_db, user: user_dependancy):
    result = await db.execute(Select(User).where(User.id == user.get("id")))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await db.delete(user)
    await db.commit()

    return {"Message": "Successfully deleted the user"}
