import logging
import os
from typing import Optional

from sqlalchemy.orm import Session

from .notification_service import create_notification
from ..models.expenseModel import Expense
from ..models import budgetModel
from ..models.budgetModel import Budget
from ..schemas.budgetSchema import BudgetCreate, BudgetUpdate
from ..models.userModel import User
from decimal import Decimal, InvalidOperation

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from ..schemas.notificationSchema import NotificationCreate, NotificationType

logging.basicConfig(level=logging.INFO)


def validate_amount(amount: Decimal):
    try:
        if amount < 0:
            raise ValueError("Amount must be greater than or equal to 0.")
        if amount.as_tuple().exponent < -2 or len(amount.as_tuple().digits) > 10:
            raise ValueError("Amount must have up to 10 digits in total and up to 2 decimal places.")
    except InvalidOperation:
        raise ValueError("Invalid amount format.")


# Create a new budget
def create_budget(budget: BudgetCreate, user_id: int, db: Session):
    validate_amount(budget.amount)

    db_budget = Budget(
        user_id=user_id,
        category=budget.category,
        amount=budget.amount,
        start_date=budget.start_date,
        end_date=budget.end_date,
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)

    # Initialize current_usage based on existing expenses within the budget's date range
    expenses = db.query(Expense).filter(
        Expense.user_id == user_id,
        Expense.category == budget.category,
        Expense.date.between(budget.start_date, budget.end_date)
    ).all()
    db_budget.current_usage = sum(expense.amount for expense in expenses)
    db.commit()
    db.refresh(db_budget)

    notify_user(db_budget, db)

    return db_budget


# Update an existing budget
def update_budget(budget_id: int, budget_update: BudgetUpdate, db: Session):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget:
        old_amount = db_budget.amount
        old_end_date = db_budget.end_date

        if budget_update.amount:
            validate_amount(budget_update.amount)
            db_budget.amount = budget_update.amount
        if budget_update.end_date:
            db_budget.end_date = budget_update.end_date

        db.commit()
        db.refresh(db_budget)

        # Recalculate current usage based on expenses within the budget's date range and category
        expenses = db.query(Expense).filter(
            Expense.user_id == db_budget.user_id,
            Expense.category == db_budget.category,
            Expense.date.between(db_budget.start_date, db_budget.end_date)
        ).all()
        db_budget.current_usage = sum(expense.amount for expense in expenses)
        db.commit()
        db.refresh(db_budget)

        notify_user(db_budget, db)

        return db_budget
    return None


# Delete a budget
def delete_budget(budget_id: int, db: Session):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget:
        # Adjust current_usage based on existing expenses within the budget's date range
        expenses = db.query(Expense).filter(
            Expense.user_id == db_budget.user_id,
            Expense.category == db_budget.category,
            Expense.date.between(db_budget.start_date, db_budget.end_date)
        ).all()
        db_budget.current_usage = sum(expense.amount for expense in expenses)
        db.delete(db_budget)
        db.commit()
    return db_budget


# Get all budgets for a user
def get_user_budgets(user_id: int, db: Session):
    return db.query(Budget).filter(Budget.user_id == user_id).all()


# New Function Added !!!!!
def is_budget_valid(user_id: int, category: str, db: Session):
    current_date = datetime.now()
    budget = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category == category,
        Budget.start_date <= current_date,
        Budget.end_date >= current_date
    ).first()
    return budget is not None


# New Function Added !!!!!
def update_budget_usage(user_id: int, category: str, db: Session, old_amount: Decimal, new_amount: Decimal, expense_date: Optional[datetime] = None):
    if expense_date:
        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == category,
            Budget.start_date <= expense_date,
            Budget.end_date >= expense_date
        ).first()
    else:
        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == category
        ).first()

    if budget:
        budget.current_usage = Decimal(budget.current_usage) - new_amount
        db.commit()
        db.refresh(budget)
        notify_user(budget, db)


# New Function Added !!!!!
def send_email(to_email: str, subject: str, body: str):
    from_email = os.getenv("EMAIL_ADDRESS")
    from_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = None
    try:
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        logging.info(f"Email sent to {to_email}")
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send email to {to_email}: {e}")
    finally:
        server.quit()


async def notify_user(budget: Budget, db: Session):
    user = db.query(User).filter(User.id == budget.user_id).first()
    if not user:
        logging.error("User not found")
        return

    user_email = user.email
    usage_percentage = (budget.current_usage / budget.amount) * 100

    if 80 <= usage_percentage < 100:
        subject = "Budget Alert: 80% Usage"
        body = f"Dear {user.name}, you have used {usage_percentage:.2f}% of your budget for {budget.category}. Please be cautious."
        send_email(user_email, subject, body)
        notification = NotificationCreate(
            type=NotificationType.BUDGET_ALERT,
            title=subject,
            message=body
        )
        create_notification(user.id, notification, db)
    elif usage_percentage >= 100:
        subject = "Budget Alert: Exceeded"
        body = f"Dear {user.name}, you have exceeded your budget for {budget.category}. Please review your expenses."
        send_email(user_email, subject, body)
        notification = NotificationCreate(
            type=NotificationType.BUDGET_ALERT,
            title=subject,
            message=body
        )
        create_notification(user.id, notification, db)

    logging.info(f"Notification sent to {user_email} for budget {budget.category}")
