from src.schemas.project_schemas import ProjectResponse
from src.schemas.user_schemas import UserResponse
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional



class CommentCreate(BaseModel):
    comment: str
    project_id: int


class OwnerDetails(BaseModel):
    id: int
    name: str

class ProjectResponseForComment(BaseModel):
    id: int
    title: str
    description: str
    # comments_count: int
    owner: OwnerDetails
    model_config = ConfigDict(from_attributes=True)

class CommentResponse(BaseModel):
    id: int
    comment: str
    created_at: datetime
    updated_at: datetime
    # user_id: int
    project: ProjectResponseForComment
    model_config = ConfigDict(from_attributes=True)

class CommentUpdate(BaseModel):
    comment: Optional[str] = None
    