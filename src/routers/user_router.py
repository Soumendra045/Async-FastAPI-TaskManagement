from sqlalchemy import Select
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


@router.post("/user_create")
@limiter.limit("10/minute")
async def create_user(user: UserCreate, db: async_db, request: Request):
    db_user = User(
        name=user.name, email=user.email, password=bcrypt.hash(user.password)
    )
    db.add(db_user)
    print(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user



@router.get("/user/{user_id}",response_model=UserResponse)
async def get_user(user_id: int, db: async_db, user: user_dependancy):
    result = await db.execute(Select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/user",response_model=UserResponse)
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


@router.delete("/user/delete")
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
