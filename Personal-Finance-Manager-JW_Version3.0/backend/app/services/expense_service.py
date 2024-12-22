from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal, InvalidOperation
from starlette import status
from starlette.exceptions import HTTPException

from ..models import expenseModel
from ..models.budgetModel import Budget
from ..models.expenseModel import Expense
from ..models.incomeModel import Income
from ..schemas.expenseSchema import ExpenseCreate, ExpenseUpdate, ExpenseCategory
from typing import Optional
from ..services.budget_service import update_budget_usage, is_budget_valid


def validate_amount(amount: Decimal):
    try:
        if amount < 0:
            raise ValueError("Amount must be greater than or equal to 0.")
        if amount.as_tuple().exponent < -2 or len(amount.as_tuple().digits) > 10:
            raise ValueError("Amount must have up to 10 digits in total and up to 2 decimal places.")
    except InvalidOperation:
        raise ValueError("Invalid amount format.")


def add_expense(expense: ExpenseCreate, user_id: int, db: Session):
    validate_amount(expense.amount)

    expense_date = datetime.now()
    db_expense = expenseModel.Expense(
        user_id=user_id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense_date,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    # Subtract expense amount from total income
    total_income = db.query(Income).filter(Income.user_id == user_id).first()
    if total_income:
        total_income.amount -= Decimal(expense.amount)
        db.commit()
        db.refresh(total_income)

    if is_budget_valid(user_id, expense.category, db):
        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == expense.category,
            Budget.start_date <= expense_date,
            Budget.end_date >= expense_date
        ).first()
        if budget:
            update_budget_usage(user_id, expense.category, db,
                                Decimal(budget.current_usage),
                                Decimal(budget.current_usage + expense.amount), expense_date)

    return db_expense


def get_expenses(user_id: int, db: Session):
    return db.query(expenseModel.Expense).filter(expenseModel.Expense.user_id == user_id).all()


def get_expense_by_id(expense_id: int, db: Session):
    return db.query(expenseModel.Expense).filter(expenseModel.Expense.id == expense_id).first()


def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session):
    validate_amount(expense.amount)

    db_expense = db.query(expenseModel.Expense).filter(expenseModel.Expense.id == expense_id).first()
    if db_expense:
        old_amount = db_expense.amount
        expense_date = db_expense.date
        db_expense.amount = expense.amount
        db_expense.category = expense.category
        db_expense.description = expense.description
        db_expense.date = expense.date or db_expense.date
        db.commit()
        db.refresh(db_expense)

        # Adjust total income
        total_income = db.query(Income).filter(Income.user_id == db_expense.user_id).first()
        if total_income:
            total_income.amount += Decimal(old_amount) - Decimal(db_expense.amount)
            db.commit()
            db.refresh(total_income)

        update_budget_usage(db_expense.user_id, db_expense.category, db, old_amount, expense.amount, expense_date)

        return db_expense
    return None


def delete_expense(expense_id: int, db: Session):
    db_expense = db.query(expenseModel.Expense).filter(expenseModel.Expense.id == expense_id).first()
    if db_expense:
        expense_date = db_expense.date
        expense_amount = db_expense.amount
        expense_category = db_expense.category
        user_id = db_expense.user_id

        db.delete(db_expense)
        db.commit()

        # Add expense amount back to total income
        total_income = db.query(Income).filter(Income.user_id == user_id).first()
        if total_income:
            total_income.amount += Decimal(expense_amount)
            db.commit()
            db.refresh(total_income)

        # Update the budget usage by adding the deleted expense amount back
        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == expense_category,
            Budget.start_date <= expense_date,
            Budget.end_date >= expense_date
        ).first()

        if budget:
            budget.current_usage = Decimal(budget.current_usage) - expense_amount
            db.commit()
            db.refresh(budget)

        return db_expense
    return None


def search_expenses(db: Session, category: Optional[ExpenseCategory] = None,
                    start_date: Optional[datetime] = None, end_date: Optional[datetime] = None,
                    amount: Optional[float] = None, user_id: Optional[int] = None,
                    expense_id: Optional[int] = None):
    query = db.query(expenseModel.Expense)

    if expense_id:
        query = query.filter(expenseModel.Expense.id == expense_id)

    if category:
        query = query.filter(expenseModel.Expense.category == category)

    if start_date and end_date:
        query = query.filter(expenseModel.Expense.date.between(start_date, end_date))
    elif start_date:
        query = query.filter(expenseModel.Expense.date >= start_date)
    elif end_date:
        query = query.filter(expenseModel.Expense.date <= end_date)

    if amount:
        query = query.filter(expenseModel.Expense.amount == amount)

    if user_id:
        query = query.filter(expenseModel.Expense.user_id == user_id)

    return query.all()