import logging

from core.typedef import UserServiceDep
from config.settings import settings

from sqlmodel import Session, SQLModel
from schemas.user import UserCreate

from config.database import engine

from services.user import UserService
from deps.user import get_user_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)
    user_service = UserService(session)
    try:
        user = user_service.get_user(settings.ADMIN_USER)
    except Exception as e:
        user = None
    if not user or not user.is_admin:
        user_in = UserCreate(
            username=settings.ADMIN_USER,
            password=settings.ADMIN_PASSWORD,
        )
        user_service.create_user(user_in, is_admin=True)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
