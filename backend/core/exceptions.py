from typing import Callable


# ------------------------------------------------------------
class BaseAPIException(Exception):
    """base exception class"""

    def __init__(self, message: str = "Service is unavailable"):
        self.message = message
        super().__init__(self.message)


# ------------------------------------------------------------
class ServiceError(BaseAPIException):
    pass


# ------------------------------------------------------------
class EntityDoesNotExistError(BaseAPIException):
    pass


# ------------------------------------------------------------
class EntityAlreadyExistsError(BaseAPIException):
    pass


# ------------------------------------------------------------
class InvalidOperationError(BaseAPIException):
    pass


# ------------------------------------------------------------
class AuthenticationFailed(BaseAPIException):
    pass


# ------------------------------------------------------------
class InvalidTokenError(BaseAPIException):
    pass
