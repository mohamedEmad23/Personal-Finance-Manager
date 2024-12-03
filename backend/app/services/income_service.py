# income_service.py
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.sql import func
from ..models import incomeModel
from ..schemas.incomeSchema import IncomeCreate, IncomeUpdate, IncomeFrequency
from typing import Optional


# Add Income
def add_income(income: IncomeCreate, user_id: int, db: Session):
    db_income = incomeModel.Income(
        user_id=user_id,
        amount=income.amount,
        description=income.description,
        frequency=income.frequency,
        source=income.source,
        created_at=func.now(),
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


# Get All Incomes for a User
def get_incomes(user_id: int, db: Session):
    return db.query(incomeModel.Income).filter(incomeModel.Income.user_id == user_id).all()


# Get Income by ID
def get_income_by_id(income_id: int, db: Session):
    return db.query(incomeModel.Income).filter(incomeModel.Income.id == income_id).first()


# Update Income
def update_income(income_id: int, income: IncomeUpdate, db: Session):
    db_income = db.query(incomeModel.Income).filter(incomeModel.Income.id == income_id).first()
    if db_income:
        db_income.amount = income.amount
        db_income.description = income.description
        db_income.frequency = income.frequency
        db_income.source = income.source
        db.commit()
        db.refresh(db_income)
        return db_income
    return None


# Delete Income
def delete_income(income_id: int, db: Session):
    db_income = db.query(incomeModel.Income).filter(incomeModel.Income.id == income_id).first()
    if db_income:
        db.delete(db_income)
        db.commit()
        return db_income
    return None


# Search Incomes
def search_incomes(
        db: Session,
        frequency: Optional[IncomeFrequency] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        amount: Optional[float] = None,
        user_id: Optional[int] = None,
        income_id: Optional[int] = None
):
    query = db.query(incomeModel.Income)

    if income_id:
        query = query.filter(incomeModel.Income.id == income_id)

    if frequency:
        query = query.filter(incomeModel.Income.frequency == frequency)

    if start_date and end_date:
        query = query.filter(incomeModel.Income.created_at.between(start_date, end_date))
    elif start_date:
        query = query.filter(incomeModel.Income.created_at >= start_date)
    elif end_date:
        query = query.filter(incomeModel.Income.created_at <= end_date)

    if amount:
        query = query.filter(incomeModel.Income.amount == amount)

    if user_id:
        query = query.filter(incomeModel.Income.user_id == user_id)

    return query.all()