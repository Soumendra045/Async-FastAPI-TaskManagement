from sqlalchemy import Select
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.database.models import Comment, Project
from typing import Annotated, List

from src.auth.auth import get_current_user
from fastapi import APIRouter

from src.schemas.comment_schemas import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter(
    prefix='/comments',
    tags=['comments']
)

db_dependancy = Annotated[AsyncSession, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

@router.post('/create',response_model=CommentResponse)
async def create_comment(comment: CommentCreate,user: user_dependancy, db: db_dependancy):

    project = await db.execute(Select(Project).where(Project.id == comment.project_id))
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


    comment_details = Comment(
        **comment.model_dump(),
        user_id=user.get('id')
    )
    
    db.add(comment_details)
    await db.commit()
    await db.refresh(comment_details)
    return comment_details

@router.get('/get-all-comments-by-project-id', response_model=List[CommentResponse])
async def all_comments(user: user_dependancy, db: db_dependancy):
    results = await db.execute(Select(Comment).where(Comment.user_id == user.get('id')))
    comments = results.scalars().all()

    return comments

@router.put('/update/{comment_id}',response_model=CommentResponse)
async def update_comment(comment: CommentUpdate, user: user_dependancy, db: db_dependancy, comment_id: int = Path(...)):
    results = await db.execute(Select(Comment).where(Comment.id == comment_id))
    comment_details = results.scalar_one_or_none()
    if not comment_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment_details.user_id != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this comment")

    comment_details.comment = comment.comment
    await db.commit()
    await db.refresh(comment_details)
    return comment_details

@router.delete('/delete/{comment_id}')
async def delete_comment(user: user_dependancy, db: db_dependancy, comment_id: int = Path(...)):
    results = await db.execute(Select(Comment).where(Comment.id == comment_id))
    comment_details = results.scalar_one_or_none()
    if not comment_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment_details.user_id != user["id"] and user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not allowed to delete this comment"
        )
    await db.delete(comment_details)
    await db.commit()
    return {"message": "Comment deleted successfully"}