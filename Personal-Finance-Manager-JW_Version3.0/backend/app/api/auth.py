# personal-finance-manager-backend/app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from ..schemas.userSchema import UserLogin, UserLoginResponse
from ..services.auth_service import authenticate_user
from ..core.database import get_db

router = APIRouter()


@router.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_result = authenticate_user(user.email, user.password, db)
    if not auth_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return UserLoginResponse(**auth_result)
