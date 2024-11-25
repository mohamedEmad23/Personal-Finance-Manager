# personal-finance-manager-backend/app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.userSchema import UserLogin
from app.services.auth_service import authenticate_user
from app.core.database import get_db

router = APIRouter()


@router.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(user.email, user.password, db)
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
