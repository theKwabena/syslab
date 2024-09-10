from sqlmodel import SQLModel, create_engine, Session

from models.user import User
from models.container import Container

DB_PATH = "/etc/unix-lab/unix-lab.db"

CONNECTION_STRING = f"sqlite:///{DB_PATH}"

CONNECTION_ARGS = {"check_same_thread": False}

engine = create_engine(CONNECTION_STRING, echo=True, connect_args=CONNECTION_ARGS)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
