from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from ..core.database import SessionLocal


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
