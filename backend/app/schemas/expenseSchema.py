from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from enum import Enum


class ExpenseCategory(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    HEALTH = "health"
    OTHER = "other"


class ExpenseBase(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    category: ExpenseCategory
    description: str
    date: datetime


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    category: Optional[ExpenseCategory] = None
    description: Optional[str] = None
    date: Optional[datetime] = None


class ExpenseInDB(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
