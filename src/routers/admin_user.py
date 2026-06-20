from src.auth.auth import get_current_user
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Annotated

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.database.models import User
from src.schemas.user_schemas import UserResponse, AdminUserUpdate




router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

async_db = Annotated[AsyncSession, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

@router.get("/all-user",response_model=List[UserResponse])
async def get_all_user(user: user_dependancy, db: async_db):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource"
        )
    results = await db.execute(Select(User))
    users = results.scalars().all()
    # print("Count:", len(users))
    # print(users)
    return users

@router.put("/update_user/{user_id}",response_model=UserResponse)
async def update_user(user_id: int, db: async_db, user: user_dependancy, user_data: AdminUserUpdate):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource"
        )
    user = await db.execute(Select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()

    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    details = user_data.model_dump(exclude_unset=True, exclude_none=True)
    
    for key, value in details.items():
        setattr(user, key, value)

    
        
    await db.commit()
    await db.refresh(user)
    return user

@router.delete('/delete_user/{user_id}')
async def delete_user(user_id: int, db: async_db, user: user_dependancy):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource"
        )
    user = await db.execute(Select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()

    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await db.delete(user)
    await db.commit()
    return {"Message": "Successfully deleted the user"}