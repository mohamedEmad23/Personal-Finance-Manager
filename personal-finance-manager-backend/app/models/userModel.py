from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.core.database import db 
# Pydantic model for user
class UserBase(BaseModel):
    email: EmailStr
    name: str
    hashed_password: str
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: str  # MongoDB uses ObjectId, so it will be a string
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# MongoDB-specific database operations
async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict['created_at'] = datetime.utcnow()
    user_dict['updated_at'] = datetime.utcnow()
    
    result = await db.users.insert_one(user_dict)  # Insert into 'users' collection
    return result.inserted_id  # Return the inserted user ID

async def get_user_by_email(email: str):
    user = await db.users.find_one({"email": email})
    return user
