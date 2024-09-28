from functools import lru_cache

from sqlmodel import SQLModel, create_engine, Session
from config.settings import settings
from models.user import User
from models.container import Container

DB_PATH = "/etc/unix-lab/unix-lab.db"

CONNECTION_STRING = f"sqlite:///{DB_PATH}"

CONNECTION_ARGS = {"check_same_thread": False}

engine = create_engine(CONNECTION_STRING, connect_args=CONNECTION_ARGS)


@lru_cache()
def get_engine():
    return create_engine(CONNECTION_STRING, connect_args=CONNECTION_ARGS)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
