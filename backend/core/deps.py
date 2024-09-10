from fastapi import Depends
from config.database import get_session
from sqlmodel import Session
from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

