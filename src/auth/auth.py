from fastapi import Depends,HTTPException, status
from typing import Annotated
from datetime import datetime,timedelta
from sqlalchemy import Select
from dotenv import load_dotenv
import os
from src.database.models import User
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db


load_dotenv('.env/.env')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

bcrypt = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')
db_dependancy = Annotated[AsyncSession, Depends(get_db)]


async def authenticated_user(username: str, password: str, db):
    user = await db.execute(Select(User).where(User.name == username))
    user = user.scalar_one_or_none()
    if not user:
        return False
    
    if not bcrypt.verify(password, user.password):
        return False
    
    return user

def create_acess_token(username: str, id: int, role: str, expkire_dlta: timedelta):
    to_encode = {'sub': username, 'id': id, 'role':role}
    expire = expkire_dlta + datetime.utcnow() 
    to_encode.update({'exp': expire})

    jwt_toekn = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_toekn

async def get_current_user(toekn: Annotated[str, Depends(oauth2_bearer)], db: db_dependancy):
    try:
        decode_token = jwt.decode(toekn, SECRET_KEY, algorithms=[ALGORITHM])
        username = decode_token.get('sub')
        id = decode_token.get('id')
        role = decode_token.get('role')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        return {'username': username, 'id': id, 'role':role}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')