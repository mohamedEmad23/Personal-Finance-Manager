from sqlalchemy.orm import Session
from app.models import userModel
from app.core.security import verify_password, create_access_token
from app.schemas.userSchema import UserLogin


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(userModel.User).filter(userModel.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return create_access_token(subject=user.id)
