from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.core.database import db  # MongoDB database connection
from app.schemas.expenseSchema import ExpenseCategory


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


# Pydantic schema for Budget
class BudgetBase(BaseModel):
    user_id: PyObjectId = Field(..., alias="user_id")  # Reference to user ID
    category: ExpenseCategory  # Budget category
    amount: float  # Budget amount
    start_date: datetime  # Budget start date
    end_date: datetime  # Budget end date
    alert_threshold: float  # Alert threshold percentage (e.g., 0.8 for 80%)
    current_usage: float = 0.0  # Current usage amount
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BudgetCreate(BudgetBase):
    pass


class BudgetInDB(BudgetBase):
    id: PyObjectId = Field(..., alias="_id")  # MongoDB uses `_id` as the primary key

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}  # Convert ObjectId to a string for JSON serialization


# MongoDB-specific database operations
async def create_budget(budget: BudgetCreate):
    budget_dict = budget.dict(by_alias=True)
    budget_dict["created_at"] = datetime.utcnow()
    budget_dict["updated_at"] = datetime.utcnow()

    result = await db.budgets.insert_one(budget_dict)  # Insert into 'budgets' collection
    return str(result.inserted_id)  # Return the inserted budget ID as a string


async def get_budget_by_id(budget_id: str):
    budget = await db.budgets.find_one({"_id": ObjectId(budget_id)})
    if budget:
        budget["_id"] = str(budget["_id"])  # Convert ObjectId to string
    return budget


async def update_budget(budget_id: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()  # Update the `updated_at` timestamp

    result = await db.budgets.update_one(
        {"_id": ObjectId(budget_id)}, {"$set": update_data}
    )
    return result.modified_count > 0  # Return True if a document was updated


async def delete_budget(budget_id: str):
    result = await db.budgets.delete_one({"_id": ObjectId(budget_id)})
    return result.deleted_count > 0  # Return True if a document was deleted
