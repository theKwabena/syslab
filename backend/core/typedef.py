from fastapi import Depends
from config.database import get_session
from sqlmodel import Session
from typing import Annotated
from deps.user import get_user_service
from deps.container import get_container_service
from services.user import UserService
from services.container import DockerService

SessionDep = Annotated[Session, Depends(get_session)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ContainerService = Annotated[DockerService, Depends(get_container_service)]
