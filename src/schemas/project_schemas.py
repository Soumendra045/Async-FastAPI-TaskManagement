from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
# from enum import Enum

class ProjectCreate(BaseModel):
    title: str
    description: str
    status: Optional[str] = 'pending'


class OwnerDetails(BaseModel):
    id: int
    name: str
    email: str

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    # comments_count: int
    owner: OwnerDetails
    model_config = ConfigDict(from_attributes=True)