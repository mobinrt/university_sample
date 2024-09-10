from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, Union
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import secrets

from DB.models import TeacherModel, StudentModel
from SCHEMA.schemas import TokenDisplay
import hash

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthServices:
    def __init__(self, session: AsyncSession, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM):
        self.session = session
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def get_user_by_id(self, user_id: int) -> Optional[Union[TeacherModel, StudentModel]]:
        user = await self.session.execute(select(TeacherModel).where(TeacherModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            user = await self.session.execute(select(StudentModel).where(StudentModel.id == user_id))
            user = user.scalar_one_or_none()
        return user

    async def get_user_by_name(self, name: str) -> Optional[Union[TeacherModel, StudentModel]]:
        user = await self.session.execute(select(TeacherModel).where(TeacherModel.name == name))
        user = user.scalar_one_or_none()
        if not user:
            user = await self.session.execute(select(StudentModel).where(StudentModel.name == name))
            user = user.scalar_one_or_none()
        return user

    async def get_token(self, request: OAuth2PasswordRequestForm) -> TokenDisplay:
        custom_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "bearer"}
        )

        user = await self.get_user_by_id(request.username)  
        if not user or not hash.verify_password(request.password, user.password):
            raise custom_error

        access_token = self.create_access_token(data={'sub': str(user.id)})  
        return TokenDisplay(access_token=access_token, token_type='bearer')

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta is None:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def get_current_user(self, token: str) -> Union[TeacherModel, StudentModel]:
        custom_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid credentials')

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")  
            if not user_id:
                raise custom_error
        except JWTError:
            raise custom_error

        user = await self.get_user_by_id(int(user_id))  
        if not user:
            raise custom_error

        return user
