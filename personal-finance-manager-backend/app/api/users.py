from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.userSchema import UserCreate, UserLogin, UserUpdate
from app.services.user_service import create_user as create_user_service, user_login, user_update, user_delete
from ..core.database import get_db
from ..core.dependencies import db_dependency
import logging
from ..services.auth_service import authenticate_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Processing data: %s", user)
        db_user = create_user_service(user, db)
        return {
            "message": "User created successfully",
            "user_id": db_user.id, }
    except Exception as e:
        logger.error("Error processing data: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR_BAD_REQUEST, detail=str(e))


@router.put("/users/{user_id}/")
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_update(user_id, user, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.delete("/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_delete(user_id, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
