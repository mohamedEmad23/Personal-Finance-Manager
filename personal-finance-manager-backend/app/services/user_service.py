from motor.motor_asyncio import AsyncIOMotorClient
from ..core.security import get_password_hash
from ..models import userModel
from ..schemas.userSchema import UserCreate
from ..core.database import get_db
from bson import ObjectId
from fastapi import HTTPException

# Get the MongoDB collection
db = get_db()
users_collection = db.users  # Assuming 'users' is the collection name in MongoDB

# Helper function to convert MongoDB ObjectId to string
def objectid_to_str(obj):
    return str(obj) if obj else None

# User Registration
async def create_user(user: UserCreate):
    # Hash the password before storing
    hashed_password = get_password_hash(user.password)
    
    # Create a new user document
    user_data = {
        "email": user.email,
        "name": user.name,
        "hashed_password": hashed_password,
        "is_active": True,
    }

    # Insert the user document into the MongoDB collection
    try:
        result = await users_collection.insert_one(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    # Fetch the inserted user (excluding sensitive data like password)
    db_user = await users_collection.find_one({"_id": result.inserted_id})
    db_user["_id"] = objectid_to_str(db_user["_id"])  # Convert ObjectId to string
    db_user.pop("hashed_password", None)  # Remove hashed password from the response
    return db_user

# User Login
async def user_login(email: str):
    # Find a user by email
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["_id"] = objectid_to_str(user["_id"])  # Convert ObjectId to string
    user.pop("hashed_password", None)  # Exclude the hashed password from the response
    return user

# User Update
async def user_update(user_id: str, user: UserCreate):
    # Find the user by ID
    db_user = await users_collection.find_one({"_id": ObjectId(user_id)})

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_data = {
        "email": user.email,
        "name": user.name,
    }

    # Hash the password only if it was changed
    if user.password:
        updated_data["hashed_password"] = get_password_hash(user.password)

    # Update the user document in MongoDB
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    
    # Return the updated user (excluding hashed password)
    db_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    db_user["_id"] = objectid_to_str(db_user["_id"])  # Convert ObjectId to string
    db_user.pop("hashed_password", None)  # Remove hashed password from the response
    return db_user

# User Delete
async def user_delete(user_id: str):
    # Delete the user by ID
    db_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await users_collection.delete_one({"_id": ObjectId(user_id)})
    
    db_user["_id"] = objectid_to_str(db_user["_id"])  # Convert ObjectId to string
    db_user.pop("hashed_password", None)  # Remove hashed password from the response
    return db_user
