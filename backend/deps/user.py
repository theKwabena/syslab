from typing import Annotated
from services.user import UserService
from fastapi import Depends
from config.database import get_session


def get_user_service(session=Depends(get_session)):
    try:
        user = UserService(session)
        yield user
    except Exception as e:
        raise e
