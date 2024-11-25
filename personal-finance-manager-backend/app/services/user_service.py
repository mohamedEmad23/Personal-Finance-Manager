from sqlalchemy.orm import Session
from ..models import userModel
from ..schemas.userSchema import UserCreate


def create_user(user: UserCreate, db: Session):
    db_user = userModel.User(
        email=user.email,
        name=user.name,
        hashed_password=user.password  # You should hash the password before storing it
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
