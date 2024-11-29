from sqlalchemy.orm import Session
from ..models import reportModel
from ..schemas.reportSchema import ReportCreate


# Create Report
def create_report(report: ReportCreate, user_id: int, file_path: str, db: Session):
    db_report = reportModel.Report(
        user_id=user_id,
        report_type=report.report_type,
        format=report.format,
        start_date=report.start_date,
        end_date=report.end_date,
        title=report.title,
        description=report.description,
        file_path=file_path,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


# Read Report by ID
def get_report_by_id(report_id: int, db: Session):
    return db.query(reportModel.Report).filter(reportModel.Report.id == report_id).first()


# Get All Reports for a User
def get_reports_by_user(user_id: int, db: Session):
    return db.query(reportModel.Report).filter(reportModel.Report.user_id == user_id).all()


# Update Report
def update_report(report_id: int, updated_report: ReportCreate, db: Session):
    db_report = db.query(reportModel.Report).filter(reportModel.Report.id == report_id).first()
    if db_report:
        db_report.report_type = updated_report.report_type
        db_report.format = updated_report.format
        db_report.start_date = updated_report.start_date
        db_report.end_date = updated_report.end_date
        db_report.title = updated_report.title
        db_report.description = updated_report.description
        db.commit()
        db.refresh(db_report)
        return db_report
    return None


# Delete Report
def delete_report(report_id: int, db: Session):
    db_report = db.query(reportModel.Report).filter(reportModel.Report.id == report_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
        return db_report
    return None
