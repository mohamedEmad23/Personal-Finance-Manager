import os
from typing import Optional

import openpyxl
from sqlalchemy.orm import Session
from ..models import reportModel
from ..models.budgetModel import Budget
from ..models.expenseModel import Expense
from ..models.incomeModel import Income
from ..schemas.reportSchema import ReportCreate, ReportType, ReportFormat

import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from openpyxl.utils import get_column_letter


# Create Report
def create_report(report: ReportCreate, user_id: int, file_path: Optional[str], file_format: ReportFormat, db: Session):
    # Set the default file path to the user's Downloads directory if not provided
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_name = f"transactions_{report.start_date.strftime('%Y%m%d')}_{report.end_date.strftime('%Y%m%d')}.{file_format}"
    file_path = os.path.join(downloads_path, file_name)

    # Generate the transactions file
    generate_transactions_file(user_id, report, file_format, db)

    # Create the report entry in the database
    db_report = reportModel.Report(
        user_id=user_id,
        report_type=report.report_type,
        format=file_format,
        start_date=report.start_date,
        end_date=report.end_date,
        title=report.title,
        description=report.description,
        file_path=file_path

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


def plot_income_expense(user_id: int, start_date: datetime, end_date: datetime, db: Session, filepath: str):
    try:
        # Query income transactions
        incomes = db.query(Income).filter(
            Income.user_id == user_id,
            Income.created_at.between(start_date, end_date)
        ).order_by(Income.created_at).all()

        # Query expense transactions
        expenses = db.query(Expense).filter(
            Expense.user_id == user_id,
            Expense.date.between(start_date, end_date)
        ).order_by(Expense.date).all()

        # Extract dates and amounts
        income_dates = [income.created_at for income in incomes]
        income_amounts = [float(income.amount) for income in incomes]
        expense_dates = [expense.date for expense in expenses]
        expense_amounts = [float(expense.amount) for expense in expenses]

        # Create plot
        plt.figure(figsize=(10, 5))
        plt.plot(income_dates, income_amounts, label='Income', color='green', marker='o')
        plt.plot(expense_dates, expense_amounts, label='Expense', color='red', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.title('Income and Expense Over Time')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot
        plt.savefig(filepath, format='png', dpi=300, bbox_inches='tight')
        plt.close()

        return filepath
    except Exception as e:
        plt.close()
        raise Exception(f"Error generating plot: {str(e)}")


def generate_transactions_file(user_id: int, report: ReportCreate, file_format: str, db: Session):
    data = []
    start_datetime = datetime.combine(report.start_date, datetime.min.time())
    end_datetime = datetime.combine(report.end_date, datetime.max.time())

    if report.report_type == ReportType.EXPENSE:
        transactions = db.query(Expense).filter(
            Expense.user_id == user_id,
            Expense.date.between(start_datetime, end_datetime)
        ).all()
        data = [{
            'Date': t.date,
            'Type': 'expense',
            'Amount': t.amount,
            'Description': t.description,
            'Category': t.category
        } for t in transactions]
    elif report.report_type == ReportType.INCOME:
        transactions = db.query(Income).filter(
            Income.user_id == user_id,
            Income.created_at.between(start_datetime, end_datetime)
        ).all()
        data = [{
            'Date': t.created_at,
            'Type': 'income',
            'Amount': t.amount,
            'Description': t.description,
            'Source': t.source,
            'Frequency': t.frequency
        } for t in transactions]
    elif report.report_type == ReportType.BUDGET:
        transactions = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.start_date.between(start_datetime, end_datetime)
        ).all()
        data = [{
            'Start Date': t.start_date,
            'End Date': t.end_date,
            'Type': 'budget',
            'Amount': t.amount,
            'Category': t.category,
            'Current Usage': t.current_usage
        } for t in transactions]
    elif report.report_type == ReportType.SUMMARY:
        expenses = db.query(Expense).filter(
            Expense.user_id == user_id,
            Expense.date.between(start_datetime, end_datetime)
        ).all()
        incomes = db.query(Income).filter(
            Income.user_id == user_id,
            Income.created_at.between(start_datetime, end_datetime)
        ).all()
        data = [{
            'Date': t.date,
            'Type': 'expense',
            'Amount': t.amount,
            'Description': t.description,
            'Category': t.category
        } for t in expenses] + [{
            'Date': t.created_at,
            'Type': 'income',
            'Amount': t.amount,
            'Description': t.description,
            'Source': t.source,
            'Frequency': t.frequency
        } for t in incomes]
        total_expense = sum(t.amount for t in expenses)
        total_income = sum(t.amount for t in incomes)
        data.append({'Total Expense': total_expense, 'Total Income': total_income})

    if file_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(f'{report.title}.csv', index=False)
    elif file_format == 'excel':
        df = pd.DataFrame(data)
        with pd.ExcelWriter(f'{report.title}.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            for col in df.select_dtypes(include=['datetime']).columns:
                col_idx = df.columns.get_loc(col) + 1
                worksheet.column_dimensions[
                    openpyxl.utils.get_column_letter(col_idx)].number_format = 'YYYY-MM-DD HH:MM:SS'
    elif file_format == 'pdf':
        c = canvas.Canvas(f'{report.title}.pdf', pagesize=letter)
        width, height = letter
        c.drawString(30, height - 30, f'{report.title}')
        y = height - 50
        for transaction in data:
            c.drawString(30, y, str(transaction))
            y -= 15
            if y < 30:
                c.showPage()
                y = height - 30
        c.save()