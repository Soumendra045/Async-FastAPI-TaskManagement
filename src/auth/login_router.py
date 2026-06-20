from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.auth.auth import create_acess_token, authenticated_user
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=["auth"]
)
db_dependancy = Annotated[AsyncSession, Depends(get_db)]

@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependancy):
    user = await authenticated_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    token = create_acess_token(user.name, user.id, user.role, timedelta(hours=1))

    return {
        'access_token': token,
        'token_type': 'Bearer'
    }

