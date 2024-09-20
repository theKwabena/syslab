from fastapi import FastAPI, APIRouter
from datetime import timedelta
from fastapi.exceptions import HTTPException
from schemas.user import UserRead, UserCreate
from core.typedef import UserServiceDep

from typing import Any
from deps.user import CurrentUser, get_current_active_superuser

from config import security
from config.settings import settings

from models.token import Token
from fastapi import Depends
from typing import Annotated

from schemas.container import UserContainer
from fastapi.security import OAuth2PasswordRequestForm
from core.typedef import ContainerService

lab_router = APIRouter(prefix="", tags=["Lab"])


@lab_router.get('/users', response_model=list[UserRead])
async def get_users(user_service: UserServiceDep):
    return user_service.get_users()


@lab_router.get('/user/{user_id}', response_model=list[UserRead])
async def get_users(user_id: str, user_service: UserServiceDep):
    return user_service.get_user(user_id)


@lab_router.delete('/user/{user_id}')
async def delete_user(user_id: str, user_service: UserServiceDep):
    return user_service.delete_user(user_id)


@lab_router.post('/users')
async def create_user(user_service: UserServiceDep, data: UserCreate):
    return user_service.create_user(data, False)


@lab_router.post('/users/admin', dependencies=[Depends(get_current_active_superuser)])
async def create_admin_user(user_service: UserServiceDep, data: UserCreate):
    return user_service.create_user(data, True)


@lab_router.post("/login/access-token")
def login_access_token(
        user_service: UserServiceDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = user_service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.username, expires_delta=access_token_expires
        )
    )


@lab_router.get("/me", )
def read_user_me(current_user: CurrentUser) -> UserRead:
    return current_user


@lab_router.get("/me/container")
def read_user_environment(current_user: CurrentUser, container_service: ContainerService):
    user_cont = container_service.get_user_environment(current_user.username)
    return user_cont
