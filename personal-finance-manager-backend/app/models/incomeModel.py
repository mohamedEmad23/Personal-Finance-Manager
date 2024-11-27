from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.core.database import db  # MongoDB database connection
from app.schemas.incomeSchema import IncomeFrequency


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


# Pydantic schema for Income
class IncomeBase(BaseModel):
    user_id: PyObjectId = Field(..., alias="user_id")  # Reference to user ID
    amount: float  # Income amount
    description: str  # Income description
    frequency: IncomeFrequency  # Income frequency
    source: str  # Income source
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IncomeCreate(IncomeBase):
    pass


class IncomeInDB(IncomeBase):
    id: PyObjectId = Field(..., alias="_id")  # MongoDB uses `_id` as the primary key

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}  # Convert ObjectId to a string for JSON serialization


# MongoDB-specific database operations
async def create_income(income: IncomeCreate):
    income_dict = income.dict(by_alias=True)
    income_dict["created_at"] = datetime.utcnow()
    income_dict["updated_at"] = datetime.utcnow()

    result = await db.incomes.insert_one(income_dict)  # Insert into 'incomes' collection
    return str(result.inserted_id)  # Return the inserted income ID as a string


async def get_income_by_id(income_id: str):
    income = await db.incomes.find_one({"_id": ObjectId(income_id)})
    if income:
        income["_id"] = str(income["_id"])  # Convert ObjectId to string
    return income


async def update_income(income_id: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()  # Update the updated_at timestamp

    result = await db.incomes.update_one(
        {"_id": ObjectId(income_id)}, {"$set": update_data}
    )
    return result.modified_count > 0  # Return True if a document was updated


async def delete_income(income_id: str):
    result = await db.incomes.delete_one({"_id": ObjectId(income_id)})
    return result.deleted_count > 0  # Return True if a document was deleted
