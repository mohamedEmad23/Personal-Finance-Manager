from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.budgetModel import Budget
from app.schemas.budgetSchema import BudgetCreate, BudgetUpdate
from app.services.budget_service import create_budget, get_user_budgets, update_budget, delete_budget
from app.core.database import get_db

budget_router = APIRouter()


@budget_router.post("/budgets/", status_code=status.HTTP_201_CREATED)
async def create_budget_endpoint(user_id: int, budget: BudgetCreate, db: Session = Depends(get_db)):
    return create_budget(budget, user_id, db)


@budget_router.get("/budgets/")
async def list_user_budgets(user_id: int, db: Session = Depends(get_db)):
    budgets = get_user_budgets(user_id, db)
    if not budgets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No budgets found for the user")
    return budgets


@budget_router.put("/budgets/{budget_id}/")
async def update_budget_endpoint(budget_id: int, budget_update: BudgetUpdate, db: Session = Depends(get_db)):
    db_budget = update_budget(budget_id, budget_update, db)
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return db_budget


@budget_router.delete("/budgets/{budget_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget_endpoint(budget_id: int, db: Session = Depends(get_db)):
    db_budget = delete_budget(budget_id, db)
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")


@budget_router.get("/budgets/{budget_id}/")
async def get_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return db_budget
