from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    type: str
    amount: condecimal(max_digits=10, decimal_places=2)
    date: datetime
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    date: Optional[datetime] = None
    description: Optional[str] = None


class TransactionInDB(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
