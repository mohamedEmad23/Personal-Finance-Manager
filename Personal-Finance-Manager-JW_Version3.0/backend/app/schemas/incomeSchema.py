from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from enum import Enum


class IncomeFrequency(str, Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class IncomeBase(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    description: Optional[str] = None
    frequency: IncomeFrequency
    source: str


class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    description: Optional[str] = None
    frequency: Optional[IncomeFrequency] = None
    source: Optional[str] = None


class IncomeInDB(IncomeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
