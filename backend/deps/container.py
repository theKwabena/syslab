from typing import Annotated
from services.user import UserService
from fastapi import Depends
from config.database import get_session
from services.container import DockerService


def get_container_service(session=Depends(get_session)):
    try:
        container_service = DockerService(session)
        yield container_service
    except Exception as e:
        raise e
