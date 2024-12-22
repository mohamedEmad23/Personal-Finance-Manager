# income.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from ..schemas.incomeSchema import IncomeCreate, IncomeUpdate
from ..services.income_service import *
from ..core.database import get_db
from typing import Optional
from datetime import datetime

income_router = APIRouter()


@income_router.post("/incomes/", status_code=status.HTTP_201_CREATED)
async def create_income(income: IncomeCreate, user_id: int, db: Session = Depends(get_db)):
    new_income = add_income(income, user_id, db)
    total_income = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).scalar()
    return {"new_income": new_income, "total_income": total_income or 0}


@income_router.put("/incomes/{income_id}/")
async def update_income_route(income_id: int, income: IncomeUpdate, db: Session = Depends(get_db)):
    db_income = update_income(income_id, income, db)
    if not db_income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return db_income


@income_router.delete("/incomes/{income_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_income_route(income_id: int, user_id: int, db: Session = Depends(get_db)):
    db_income = delete_income(income_id, db)
    if not db_income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    total_income = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).scalar()
    return {"total_income": total_income or 0}


@income_router.get("/incomes/search/")
async def search_incomes_route(frequency: Optional[str] = None, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None, amount: Optional[float] = None,
                               user_id: Optional[int] = None, income_id: Optional[int] = None,
                               db: Session = Depends(get_db)):
    return search_incomes(db, frequency, start_date, end_date, amount, user_id, income_id)


@income_router.get("/income/incomes")
async def get_all_incomes(user_id: int, db: Session = Depends(get_db)):
    incomes = get_incomes(user_id, db)
    if not incomes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No budgets found for the user")
    return incomes


# income.py
@income_router.get("/incomes/total")
async def get_total_income(user_id: int, db: Session = Depends(get_db)):
    total_income = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).scalar()
    return {"total_income": total_income or 0}
