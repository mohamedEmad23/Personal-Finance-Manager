from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.schemas.budgetSchema import BudgetCreate, BudgetUpdate
from app.services.budget_service import (
    create_budget as create_budget_service,
    update_budget as update_budget_service,
    delete_budget as delete_budget_service,
    get_user_budgets,
    update_budget_usage as update_budget_usage_service,
)
from app.core.database import get_db

router = APIRouter()


#create a new budget for the user
@router.post("/budgets/", status_code=status.HTTP_201_CREATED)
async def create_budget(user_id: int, budget: BudgetCreate, db: Session = Depends(get_db)):

    return create_budget_service(budget, user_id, db)


#get all the budgets for a user
@router.get("/budgets/")
async def list_user_budgets(user_id: int, db: Session = Depends(get_db)):

    budgets = get_user_budgets(user_id, db)
    if not budgets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No budgets found for the user")
    return budgets


#update an existing budget
@router.put("/budgets/{budget_id}/")
async def update_budget(budget_id: int, budget_update: BudgetUpdate, db: Session = Depends(get_db)):

    db_budget = update_budget_service(budget_id, budget_update, db)
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return db_budget


#delete a budget using its id
@router.delete("/budgets/{budget_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(budget_id: int, db: Session = Depends(get_db)):

    db_budget = delete_budget_service(budget_id, db)
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")


