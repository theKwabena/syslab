from fastapi import FastAPI, APIRouter
from schemas.user import UserRead, UserCreate
from core.typedef import ContainerService

container_router = APIRouter(prefix="", tags=["Lab"])


@container_router.post('/container')
async def create_container(container_service: ContainerService):
    return container_service.create_container("abbey")

