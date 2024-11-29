from sqlalchemy.orm import Session
from app.models.budgetModel import Budget
from app.schemas.budgetSchema import BudgetCreate, BudgetUpdate


# Create a new budget
def create_budget(budget: BudgetCreate, user_id: int, db: Session):
    db_budget = Budget(
        user_id=user_id,
        category=budget.category,
        amount=budget.amount,
        start_date=budget.start_date,
        end_date=budget.end_date,
        alert_threshold=budget.alert_threshold,
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


# Update an existing budget
def update_budget(budget_id: int, budget_update: BudgetUpdate, db: Session):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not db_budget:
        return None

    if budget_update.amount:
        db_budget.amount = budget_update.amount
    if budget_update.alert_threshold:
        db_budget.alert_threshold = budget_update.alert_threshold
    if budget_update.end_date:
        db_budget.end_date = budget_update.end_date

    db.commit()
    db.refresh(db_budget)
    return db_budget


# Delete a budget
def delete_budget(budget_id: int, db: Session):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget:
        db.delete(db_budget)
        db.commit()
    return db_budget


# Get all budgets for a user
def get_user_budgets(user_id: int, db: Session):
    return db.query(Budget).filter(Budget.user_id == user_id).all()





# Notify user if the alert threshold is crossed
def alert_user(budget_id: int, db: Session):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget and (db_budget.current_usage / db_budget.amount) * 100 >= db_budget.alert_threshold:
        # Logic to send notification goes here
        #to call notification_service later
        print(f"Alert: Budget threshold exceeded for {db_budget.category}")


    