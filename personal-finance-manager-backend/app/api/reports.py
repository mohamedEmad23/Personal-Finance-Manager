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
)

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


# Create Report
@router.post("/", response_model=ReportInDB)
def create_new_report(
    report: ReportCreate, 
    user_id: int, 
    file_path: str, 
    db: Session = Depends(get_db)
):
    return create_report(report, user_id, file_path, db)


# Get Report by ID
@router.get("/{report_id}", response_model=ReportInDB)
def get_report(report_id: int, db: Session = Depends(get_db)):
    db_report = get_report_by_id(report_id, db)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report


# Get All Reports for a User
@router.get("/user/{user_id}", response_model=List[ReportInDB])
def get_all_reports(user_id: int, db: Session = Depends(get_db)):
    return get_reports_by_user(user_id, db)


# Update Report
@router.put("/{report_id}", response_model=ReportInDB)
def update_existing_report(
    report_id: int, 
    updated_report: ReportCreate, 
    db: Session = Depends(get_db)
):
    db_report = update_report(report_id, updated_report, db)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report


# Delete Report
@router.delete("/{report_id}", response_model=ReportInDB)
def delete_existing_report(report_id: int, db: Session = Depends(get_db)):
    db_report = delete_report(report_id, db)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report
