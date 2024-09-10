from fastapi import FastAPI, APIRouter
from schemas.user import UserRead, UserCreate
from core.typedef import UserServiceDep

lab_router = APIRouter(prefix="", tags=["Lab"])

@lab_router.get('/users', response_model=list[UserRead])
async def get_users(user_service: UserServiceDep):
    return user_service.get_users()


@lab_router.post('/users')
async def create_user(user_service: UserServiceDep, data: UserCreate):
    return user_service.create_user(data)


# @lab_router.get("/containers", response_model=list[UserRead])
# async def get_containers(session: SessionDep):
#     return UserService
