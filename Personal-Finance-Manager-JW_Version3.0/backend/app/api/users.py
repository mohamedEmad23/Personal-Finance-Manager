from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.userSchema import UserCreate, UserLogin, UserUpdate
from ..services.user_service import create_user as create_user_service, get_user_by_id, user_update, user_delete
from ..core.database import get_db
from ..core.dependencies import db_dependency

from ..services.auth_service import authenticate_user

router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)


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


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user:
        return {"id": user.id, "name": user.name}
    else:
        return {"error": "User not found"}