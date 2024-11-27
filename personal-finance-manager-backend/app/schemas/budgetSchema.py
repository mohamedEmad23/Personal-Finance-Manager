from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from app.schemas.expenseSchema import ExpenseCategory


class BudgetBase(BaseModel):
    category: ExpenseCategory
    amount: condecimal(max_digits=10, decimal_places=2) # type: ignore
    start_date: datetime
    end_date: datetime
    alert_threshold: condecimal(max_digits=3, decimal_places=2)  # Percentage # type: ignore


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore
    alert_threshold: Optional[condecimal(max_digits=3, decimal_places=2)] = None  # type: ignore
    end_date: Optional[datetime] = None


class BudgetInDB(BudgetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    current_usage: condecimal(max_digits=10, decimal_places=2)  # type: ignore

    class Config:
        from_attributes = True
