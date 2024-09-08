from sqlmodel import SQLModel, create_engine
from . import models


sqlite_file_name = "database/unix-lab.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)