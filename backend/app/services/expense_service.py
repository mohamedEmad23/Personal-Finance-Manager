from sqlalchemy.orm import Session
from datetime import datetime
from ..models import expenseModel
from ..schemas.expenseSchema import ExpenseCreate, ExpenseUpdate, ExpenseCategory
from typing import Optional


def add_expense(expense: ExpenseCreate, user_id: int, db: Session):
    db_expense = expenseModel.Expense(
        user_id=user_id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=datetime.now(),
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(user_id: int, db: Session):
    return db.query(expenseModel.Expense).filter(expenseModel.Expense.user_id == user_id).all()


def get_expense_by_id(expense_id: int, db: Session):
    return db.query(expenseModel.Expense).filter(expenseModel.Expense.id == expense_id).first()


def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session):
    db_expense = db.query(expenseModel.Expense).filter(expenseModel.Expense.id == expense_id).first()
    if db_expense:
        db_expense.amount = expense.amount
        db_expense.category = expense.category
        db_expense.description = expense.description
        db_expense.date = expense.date or db_expense.date
        db.commit()
        db.refresh(db_expense)
        return db_expense
    return None


def delete_expense(expense_id: int, db: Session):
    db_expense = db.query(expenseModel.Expense).filter(expenseModel.Expense.id == expense_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
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