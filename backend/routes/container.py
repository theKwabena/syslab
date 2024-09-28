from fastapi import FastAPI, APIRouter
from schemas.user import UserRead, UserCreate
from core.typedef import ContainerService

container_router = APIRouter(prefix="", tags=["Lab"])


@container_router.post('/container')
async def create_container(container_service: ContainerService):
    return container_service.create_container("abbey")


@container_router.get('/container')
async def get_container(container_service: ContainerService):
    return container_service.list_host_containers()


@container_router.get('/user-containers')
async def get_containers(container_service: ContainerService):
    return container_service.list_user_containers()
