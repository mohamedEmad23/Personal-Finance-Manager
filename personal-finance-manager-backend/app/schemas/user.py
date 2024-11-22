from sqlalchemy import Column, Integer, String, BIGINT, Boolean, TEXT
from sqlalchemy.orm import validates
from sqlalchemy.event import listen
from ..core.database import Base
import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(TEXT, nullable=False)

    @validates('password')
    def validate_password(self, key, password):
        return hash_password(password)


# Ensure password is hashed before insert and update
def hash_password_before_insert(mapper, connection, target):
    target.password = target.hash_password(target.password)


listen(User, 'before_insert', hash_password_before_insert)
listen(User, 'before_update', hash_password_before_insert)


