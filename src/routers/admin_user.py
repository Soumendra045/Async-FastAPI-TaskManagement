from src.auth.auth import get_current_user
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Annotated

from sqlalchemy import Select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.database.models import User, Project
from src.schemas.user_schemas import UserResponse, AdminUserUpdate
from src.schemas.project_schemas import ProjectResponse




router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

async_db = Annotated[AsyncSession, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

@router.get("/all-user",response_model=List[UserResponse])
async def get_all_user(
    user: user_dependancy,
    db: async_db,
    skip: int = 0,
    limit: int = 10
    ):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource"
        )
    results = await db.execute(Select(User).offset(skip).limit(limit))
    users = results.scalars().all()
    # print("Count:", len(users))
    # print(users)
    return users

@router.get("/user/{user_id}",response_model=UserResponse)
async def get_user(user_id: int, db: async_db, user: user_dependancy):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource"
        )
    result = await db.execute(Select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

@router.put("/update_user/{user_id}",response_model=UserResponse)
async def update_user(user_id: int, db: async_db, user: user_dependancy, user_data: AdminUserUpdate):
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


@router.get("/search_user", response_model=List[UserResponse])
async def search_user(
    query: str,
    db: async_db,
    user: user_dependancy,
    skip: int=0,
    limit: int=10
):

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource"
        )
    query = query.strip()
    results = await db.execute(Select(User).where(or_(
        User.name.ilike(f"%{query}%"),
        User.email.ilike(f"%{query}%")
    )).offset(skip).limit(limit))

    users = results.scalars().all()

    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return users

@router.get('/seaarch_projects', response_model=List[ProjectResponse])
async def search_projects(
    query: str,
    db: async_db,
    user: user_dependancy,
    skip: int = 0,
    limit: int = 100
):

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource"
        )
    query = query.strip()
    results = await db.execute(Select(Project).where(
        or_(
            Project.title.ilike(f"%{query}%"),
            Project.description.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit))

    projects = results.scalars().all()
    if projects is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return projects