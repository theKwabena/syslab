from typing import Callable
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from .exceptions import BaseAPIException, EntityDoesNotExistError, EntityAlreadyExistsError, AuthenticationFailed, ServiceError
from fastapi import FastAPI, Request, status


def create_exception_handler(status_code: int, initial_detail: str) -> Callable[
    [Request, BaseAPIException], JSONResponse
]:
    detail = {"message": initial_detail}

    async def exception_handler(_: Request, exc: BaseAPIException) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(EntityDoesNotExistError, create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND, initial_detail="Entity does not exist"
    ))

    app.add_exception_handler(EntityAlreadyExistsError, create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST, initial_detail="Entity already exists"
    ))

    app.add_exception_handler(ServiceError, create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, initial_detail="An error occurred. Code: E1001"
    ))

    app.add_exception_handler(AuthenticationFailed, create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,initial_detail="Authentication Failed"
    ))
