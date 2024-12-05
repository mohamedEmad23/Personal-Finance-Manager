from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from ..schemas.expenseSchema import ExpenseCreate, ExpenseUpdate
from ..services.expense_service import *
from ..core.database import get_db
from typing import Optional

expense_router = APIRouter()


@expense_router.post("/expenses/", status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreate, user_id: int, db: Session = Depends(get_db)):
    return add_expense(expense, user_id, db)


@expense_router.put("/expenses/{expense_id}/")
async def update_expense_route(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = update_expense(expense_id, expense, db)
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return db_expense


@expense_router.delete("/expenses/{expense_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense_route(expense_id: int, db: Session = Depends(get_db)):
    db_expense = delete_expense(expense_id, db)
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")


@expense_router.get("/expenses/search/")
async def search_expenses_route(category: Optional[str] = None, start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None, amount: Optional[float] = None,
                                user_id: Optional[int] = None, expense_id: Optional[int] = None,
                                db: Session = Depends(get_db)):
    return search_expenses(db, category, start_date, end_date, amount, user_id, expense_id)


@expense_router.get("/expenses/")
async def get_all_expenses(user_id: int, db: Session = Depends(get_db)):
    expenses = get_expenses(user_id, db)
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No budgets found for the user")
    return expenses