import jwt
from typing import Annotated
from services.user import UserService
from fastapi import Depends
from config.database import get_session
from config.settings import settings
from config import security

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from models.token import TokenPayload, Token
from models.user import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_user_service(session=Depends(get_session)):
    try:
        user = UserService(session)
        yield user
    except Exception as e:
        raise e


def get_current_user(token: TokenDep, user_service: UserService = Depends(get_user_service)) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_service.get_user(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
