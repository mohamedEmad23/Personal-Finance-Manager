from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.core.database import db  # MongoDB database connection
from app.schemas.notificationSchema import NotificationType


# MongoDB-specific Pydantic model for ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Pydantic schema for Notification
class NotificationBase(BaseModel):
    user_id: PyObjectId
    type: NotificationType
    title: str
    message: str
    is_read: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationInDB(NotificationBase):
    id: PyObjectId
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}  # Ensure ObjectId is converted to a string


# MongoDB-specific database operations
async def create_notification(notification: NotificationCreate):
    notification_dict = notification.dict()
    notification_dict["created_at"] = datetime.utcnow()
    notification_dict["updated_at"] = datetime.utcnow()

    result = await db.notifications.insert_one(notification_dict)  # Insert into 'notifications' collection
    return str(result.inserted_id)  # Return the inserted notification ID as a string


async def get_notification_by_id(notification_id: str):
    notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    if notification:
        notification["_id"] = str(notification["_id"])  # Convert ObjectId to string
    return notification


async def update_notification(notification_id: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()  # Update the updated_at timestamp

    result = await db.notifications.update_one(
        {"_id": ObjectId(notification_id)}, {"$set": update_data}
    )
    return result.modified_count > 0  # Return True if a document was updated


async def delete_notification(notification_id: str):
    result = await db.notifications.delete_one({"_id": ObjectId(notification_id)})
    return result.deleted_count > 0  # Return True if a document was deleted
