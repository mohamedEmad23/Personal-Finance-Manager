from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette import status

from ..models.budgetModel import Budget
from ..schemas.budgetSchema import BudgetCreate, BudgetUpdate
from ..services.budget_service import create_budget, get_user_budgets, update_budget, delete_budget, \
    update_budget_usage, send_email, notify_user
from ..core.database import get_db

budget_router = APIRouter()


class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str


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

    # Update budget usage if necessary
    if budget_update.amount:
        update_budget_usage(db_budget.user_id, db_budget.category, db, db_budget.current_usage, db_budget.current_usage)

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


@budget_router.post("/send-email/", status_code=200)
async def send_email_endpoint(email_request: EmailRequest, db: Session = Depends(get_db)):
    try:
        send_email(email_request.to_email, email_request.subject, email_request.body)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
