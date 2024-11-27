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


# Pydantic schema for Expense
class ExpenseBase(BaseModel):
    user_id: PyObjectId = Field(..., alias="user_id")  # Reference to user ID
    amount: float  # Expense amount
    category: ExpenseCategory  # Expense category
    description: str  # Expense description
    date: datetime  # Date of the expense
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseInDB(ExpenseBase):
    id: PyObjectId = Field(..., alias="_id")  # MongoDB uses `_id` as the primary key

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}  # Convert ObjectId to a string for JSON serialization


# MongoDB-specific database operations
async def create_expense(expense: ExpenseCreate):
    expense_dict = expense.dict(by_alias=True)
    expense_dict["created_at"] = datetime.utcnow()
    expense_dict["updated_at"] = datetime.utcnow()

    result = await db.expenses.insert_one(expense_dict)  # Insert into 'expenses' collection
    return str(result.inserted_id)  # Return the inserted expense ID as a string


async def get_expense_by_id(expense_id: str):
    expense = await db.expenses.find_one({"_id": ObjectId(expense_id)})
    if expense:
        expense["_id"] = str(expense["_id"])  # Convert ObjectId to string
    return expense


async def update_expense(expense_id: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()  # Update the updated_at timestamp

    result = await db.expenses.update_one(
        {"_id": ObjectId(expense_id)}, {"$set": update_data}
    )
    return result.modified_count > 0  # Return True if a document was updated


async def delete_expense(expense_id: str):
    result = await db.expenses.delete_one({"_id": ObjectId(expense_id)})
    return result.deleted_count > 0  # Return True if a document was deleted