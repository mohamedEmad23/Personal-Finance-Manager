from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..schemas.reportSchema import ReportCreate, ReportInDB
from ..services.report_service import (
    create_report,
    get_report_by_id,
    get_reports_by_user,
    update_report,
    delete_report,
    plot_income_expense,
    generate_transactions_file
)

report_router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


# Create Report
@report_router.post("/", response_model=ReportInDB)
def create_new_report(
    report: ReportCreate,
    user_id: int,
    file_path: str,
    file_format: str,
    db: Session = Depends(get_db)
):
    return create_report(report, user_id, file_path, file_format, db)


# # Get Report by ID
# @report_router.get("/{report_id}", response_model=ReportInDB)
# def get_report(report_id: int, db: Session = Depends(get_db)):
#     db_report = get_report_by_id(report_id, db)
#     if not db_report:
#         raise HTTPException(status_code=404, detail="Report not found")
#     return db_report


# Get All Reports for a User
@report_router.get("/user/{user_id}", response_model=List[ReportInDB])
def get_all_reports(user_id: int, db: Session = Depends(get_db)):
    return get_reports_by_user(user_id, db)


# # Update Report
# @report_router.put("/{report_id}", response_model=ReportInDB)
# def update_existing_report(
#     report_id: int,
#     updated_report: ReportCreate,
#     db: Session = Depends(get_db)
# ):
#     db_report = update_report(report_id, updated_report, db)
#     if not db_report:
#         raise HTTPException(status_code=404, detail="Report not found")
#     return db_report


# Delete Report
@report_router.delete("/{report_id}", response_model=ReportInDB)
def delete_existing_report(report_id: int, db: Session = Depends(get_db)):
    db_report = delete_report(report_id, db)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report


@report_router.get("/plot_income_expense/")
def plot_income_expense_endpoint(user_id: int, start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    plot_income_expense(user_id, start_date, end_date, db)
    return {"message": "Plot generated successfully"}


@report_router.get("/generate_transactions_file/")
def generate_transactions_file_endpoint(user_id: int, year: int, file_format: str, db: Session = Depends(get_db)):
    if file_format not in ['csv', 'excel', 'pdf']:
        raise HTTPException(status_code=400, detail="Invalid file format")
    generate_transactions_file(user_id, year, file_format, db)
    return {"message": f"Transactions file generated successfully in {file_format} format"}