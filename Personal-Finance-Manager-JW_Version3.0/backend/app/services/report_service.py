import os

from sqlalchemy.orm import Session
from ..models import reportModel
from ..schemas.reportSchema import ReportCreate

import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.transactionModel import Transaction

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from ..models.transactionModel import Transaction


# Create Report
def create_report(report: ReportCreate, user_id: int, file_path: str, file_format: str, db: Session):
    # Set the default file path to the user's Downloads directory if not provided
    if not file_path:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        file_name = f"transactions_{report.start_date.strftime('%Y%m%d')}_{report.end_date.strftime('%Y%m%d')}.{file_format}"
        file_path = os.path.join(downloads_path, file_name)

    # Generate the transactions file
    generate_transactions_file(user_id, report.start_date.year, file_format, db)

    # Create the report entry in the database
    db_report = reportModel.Report(
        user_id=user_id,
        report_type=report.report_type,
        format=file_format,
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


def plot_income_expense(user_id: int, start_date: datetime, end_date: datetime, db: Session):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()

    dates = [t.date for t in transactions]
    amounts = [t.amount for t in transactions]
    types = [t.type for t in transactions]

    income_dates = [dates[i] for i in range(len(types)) if types[i] == 'income']
    income_amounts = [amounts[i] for i in range(len(types)) if types[i] == 'income']
    expense_dates = [dates[i] for i in range(len(types)) if types[i] == 'expense']
    expense_amounts = [amounts[i] for i in range(len(types)) if types[i] == 'expense']

    plt.figure(figsize=(10, 5))
    plt.plot(income_dates, income_amounts, label='Income', color='green')
    plt.plot(expense_dates, expense_amounts, label='Expense', color='red')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expense Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('income_expense_plot.png')
    plt.close()


def generate_transactions_file(user_id: int, year: int, file_format: str, db: Session):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date.between(f'{year}-01-01', f'{year}-12-31')
    ).all()

    data = [{
        'Date': t.date,
        'Type': t.type,
        'Amount': t.amount,
        'Description': t.description
    } for t in transactions]

    if file_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(f'transactions_{year}.csv', index=False)
    elif file_format == 'excel':
        df = pd.DataFrame(data)
        df.to_excel(f'transactions_{year}.xlsx', index=False)
    elif file_format == 'pdf':
        c = canvas.Canvas(f'transactions_{year}.pdf', pagesize=letter)
        width, height = letter
        c.drawString(30, height - 30, f'Transactions for {year}')
        y = height - 50
        for transaction in data:
            c.drawString(30, y,
                         f"{transaction['Date']} - {transaction['Type']} - {transaction['Amount']} - {transaction['Description']}")
            y -= 15
            if y < 30:
                c.showPage()
                y = height - 30
        c.save()
