from typing import Annotated
from fastapi import Depends
from services.user import UserService
from deps.user import get_user_service

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
