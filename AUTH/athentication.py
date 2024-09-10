from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, status, Depends
from typing import Union
from fastapi.security import OAuth2PasswordBearer

from DB.models import TeacherModel, StudentModel
from AUTH.auth_services import AuthServices
from SCHEMA.schemas import TokenDisplay, UserDisplay
from dependencies import get_auth_service

router = APIRouter(tags=['authentication'])
oauth2_sc = OAuth2PasswordBearer(tokenUrl='token')

@router.post('/token', response_model=TokenDisplay, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    auth_service: AuthServices = Depends(get_auth_service)
):
    return await auth_service.get_token(form_data)

@router.get("/dev-login-token")
async def get_dev_token(auth_service: AuthServices = Depends(get_auth_service)):
    token = auth_service.create_access_token(data={"sub": "dev_user"})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/read/users/me", response_model=UserDisplay)
async def read_users_me(token: str = Depends(oauth2_sc), auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.get_current_user(token)