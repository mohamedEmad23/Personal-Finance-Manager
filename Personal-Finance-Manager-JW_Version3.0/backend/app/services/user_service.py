from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..models import userModel
from ..schemas.userSchema import UserCreate


# User Registration
def create_user(user: UserCreate, db: Session):
    db_user = userModel.User(
        email=user.email,
        name=user.name,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# User Login
def user_login(email: str, db: Session):
    user = db.query(userModel.User).filter(userModel.User.email == email).first()
    return user


# api

# User Update
def user_update(user_id: int, user: UserCreate, db: Session):
    db_user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    if db_user:
        db_user.email = user.email
        db_user.name = user.name
        db_user.hashed_password = get_password_hash(user.password)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


# User Delete
def user_delete(user_id: int, db: Session):
    db_user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

# User should be able to register on the website and create a new account


def get_user_by_id(db: Session, user_id: int):
    return db.query(userModel.User).filter(userModel.User.id == user_id).first()