from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(... ,min_length=3 ,max_length=50,unique=True)
    email: EmailStr
    password: str = Field(... ,min_length=8 ,max_length=100)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None ,min_length=3 ,max_length=50)
    email: Optional[str] = None
    password: Optional[str] = Field(None ,min_length=8 ,max_length=100)

class ProjectDetails(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime


    model_config  = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(UserResponse):
    projects: List[ProjectDetails]

    model_config = ConfigDict(from_attributes=True)


class AdminUserUpdate(BaseModel):
    name: Optional[str] = Field(None ,min_length=3 ,max_length=50)
    email: Optional[str] = None
    password: Optional[str] = Field(None ,min_length=8 ,max_length=100)
    role: Optional[str] = None