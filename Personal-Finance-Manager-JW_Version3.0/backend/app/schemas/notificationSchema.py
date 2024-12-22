from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    BUDGET_ALERT = "budget_alert"
    BILL_DUE = "bill_due"
    GOAL_REACHED = "goal_reached"
    SYSTEM = "system"


class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    message: str
    is_read: bool = False


class NotificationCreate(NotificationBase):
    title: str
    message: str


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationInDB(NotificationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
