from sqlalchemy import Select
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.database.models import Project
from typing import Annotated, List

from src.auth.auth import get_current_user
from fastapi import APIRouter

from src.schemas.project_schemas import ProjectCreate, ProjectResponse


router = APIRouter(
    prefix='/projects',
    tags=['projects']
)


db_dependancy = Annotated[AsyncSession, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

@router.post('/create', response_model=ProjectResponse)
async def create_project(project: ProjectCreate, user: user_dependancy, db: db_dependancy):
    project_details = Project(
        **project.model_dump(),
        owner_id=user.get('id')
    )

    db.add(project_details)
    await db.commit()
    await db.refresh(project_details)

    return project_details


@router.get('/all-projects', response_model=List[ProjectResponse])
async def all_projects(user: user_dependancy, db: db_dependancy):
    results = await db.execute(Select(Project).where(Project.owner_id == user.get('id')))
    projects = results.scalars().all()

    return projects

@router.get('/get-by-id/{project_id}', response_model=ProjectResponse)
async def get_by_project_id( user: user_dependancy, db: db_dependancy,project_id: int = Path(...,ge=1)):
    results = await db.execute(Select(Project).where(Project.id == project_id, Project.owner_id == user.get('id')))
    project =  results.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    return project

# @router.put()