from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..schemas.userSchema import UserCreate, UserLogin, UserUpdate
from app.services.user_service import create_user as create_user_service, user_login, user_update, user_delete
from ..core.database import get_db  # MongoDB client
from ..services.auth_service import authenticate_user

router = APIRouter()

# Now, the get_db function returns the MongoDB database object directly
# The MongoDB operations will be asynchronous

# Create user
@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):  
    return await create_user_service(user)

# Update user
@router.put("/users/{user_id}/")
async def update_user(user_id: str, user: UserUpdate):  # Use string ID for MongoDB
    db_user = await user_update(user_id, user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

# Delete user
@router.delete("/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):  # Use string ID for MongoDB
    db_user = await user_delete(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "User deleted successfully"}
