from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ReportType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    BUDGET = "budget"
    SUMMARY = "summary"


class ReportFormat(str, Enum):
    PDF = "pdf"
    CSV = "csv"
    EXCEL = "excel"


class ReportBase(BaseModel):
    report_type: ReportType
    format: ReportFormat
    start_date: datetime
    end_date: datetime
    title: str
    description: Optional[str] = None


class ReportCreate(ReportBase):
    report_type: ReportType
    start_date: datetime
    end_date: datetime
    title: Optional[str] = None
    description: Optional[str] = None
    format: ReportFormat


class ReportInDB(ReportBase):
    id: int
    user_id: int
    created_at: datetime
    file_path: Optional[str]
    format: ReportFormat

    class Config:
        from_attributes = True
