from sqlalchemy.orm import Session
from ..models import userModel
from ..core.security import verify_password, create_access_token
from ..schemas.userSchema import UserLogin


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(userModel.User).filter(userModel.User.email == email).first()
    if user and verify_password(password, user.hashed_password):  # Verify password logic
        token = create_access_token(user.id)  # Token generation logic
        return {"token": token, "user_id": user.id}  # Return required data
    return None