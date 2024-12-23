from datetime import datetime
from fastapi.staticfiles import StaticFiles
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..machineLearning.budget_recommendation_model import BudgetAnalyzer
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

report_router = APIRouter()

# Create plots directory if it doesn't exist
PLOTS_DIR = "static/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


# Create Report
# @report_router.post("/", response_model=ReportInDB)
# async def create_new_report(
#    report: ReportCreate,
#     user_id: int,
#     file_path: Optional[str] = None,
#     description: Optional[str] = None,
#     title: Optional[str] = None,
#     file_format: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     return create_report(report, user_id, file_path, description, title, file_format, db)
@report_router.post("/", response_model=ReportInDB)
async def create_new_report(
    report: ReportCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    # Validate required fields
    if not report.start_date:
        raise HTTPException(
            status_code=400,
            detail="start_date is required"
        )
    if not report.end_date:
        raise HTTPException(
            status_code=400,
            detail="end_date is required"
        )
    
    # The file_path and format are now handled within the service
    try:
        return create_report(
            report=report,
            user_id=user_id,
            file_path=None,  # This will be generated in the service
            file_format=report.format,  # Use the format from the report object
            db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create report: {str(e)}"
        )


# # Get Report by ID
# @report_router.get("/{report_id}", response_model=ReportInDB)
# def get_report(report_id: int, db: Session = Depends(get_db)):
#     db_report = get_report_by_id(report_id, db)
#     if not db_report:
#         raise HTTPException(status_code=404, detail="Report not found")
#     return db_report


# Get All Reports for a User
@report_router.get("/user/{user_id}", response_model=List[ReportInDB])
async def get_all_reports(user_id: int, db: Session = Depends(get_db)):
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
async def delete_existing_report(report_id: int, db: Session = Depends(get_db)):
    db_report = delete_report(report_id, db)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report


@report_router.get("/plot_income_expense/")
async def plot_income_expense_endpoint(
    user_id: int, 
    start_date: datetime, 
    end_date: datetime, 
    db: Session = Depends(get_db)
):
    try:
        # Generate unique filename
        filename = f"income_expense_plot_{user_id}_{int(datetime.now().timestamp())}.png"
        filepath = os.path.join(PLOTS_DIR, filename)
        
        # Generate and save plot
        plot_income_expense(user_id, start_date, end_date, db, filepath)
        
        # Return plot URL
        plot_url = f"/static/plots/{filename}"
        return {"plot_url": plot_url, "message": "Plot generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@report_router.get("/generate_transactions_file/")
async def generate_transactions_file_endpoint(user_id: int, report: ReportCreate, file_format: str, db: Session = Depends(get_db)):
    if file_format not in ['csv', 'excel', 'pdf']:
        raise HTTPException(status_code=400, detail="Invalid file format")
    generate_transactions_file(user_id, report, file_format, db)
    return {"message": f"Transactions file generated successfully in {file_format} format"}


# routes/ml_routes.py
@report_router.post("/analyze-spending/{user_id}")
async def analyze_spending(user_id: int, db: Session = Depends(get_db)):
    """
    Analyze user spending and generate budget recommendations and visualizations.

    Args:
        user_id (int): The ID of the user.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing recommendations and visualizations.
    """
    analyzer = BudgetAnalyzer(db)
    training_result = analyzer.train_model(user_id)

    if "error" in training_result:
        raise HTTPException(status_code=400, detail=training_result["error"])

    recommendations = analyzer.generate_recommendations(user_id)
    visualizations = analyzer.generate_visualization(user_id)

    return {
        "recommendations": recommendations,
        "visualizations": visualizations,
        "training_result": training_result
    }