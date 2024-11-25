from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.userSchema import UserCreate
from app.services.user_service import create_user as create_user_service
from ..core.database import get_db
from ..core.dependencies import db_dependency

router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)
