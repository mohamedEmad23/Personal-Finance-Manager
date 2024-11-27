from app.core.security import verify_password, create_access_token
from app.models import userModel
from bson.objectid import ObjectId


async def authenticate_user(email: str, password: str, db):
    # Find the user in the MongoDB 'users' collection
    user = await userModel.users.find_one({"email": email})   
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    access_token = create_access_token(data={"sub": str(user["_id"])})  # Ensure ObjectId is converted to string
    return access_token
