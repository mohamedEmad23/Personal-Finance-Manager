import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from decimal import Decimal
from ..core.database import Base, get_db
from ..main import app
from ..models.budgetModel import Budget
from ..schemas.budgetSchema import BudgetCreate, BudgetUpdate

# Configure test database
SQLALCHEMY_DATABASE_URL = "mysql://root:123Main_Connection123@localhost/finance_manager_sp"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Integration Test Cases
def test_create_budget():
    budget_data = {
        "category": "food",
        "amount": "500.00",
        "start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
    user_id = 1

    response = client.post(f"/budgets/?user_id={user_id}", json=budget_data)

    assert response.status_code == 201
    created_budget = response.json()
    assert created_budget["amount"] == "500.00"
    assert created_budget["category"] == "food"
    assert created_budget["user_id"] == user_id

def test_update_budget():
    # First, create a budget entry to update
    budget_data = {
        "category": "food",
        "amount": "500.00",
        "start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
    user_id = 1

    create_response = client.post(f"/budgets/?user_id={user_id}", json=budget_data)

    assert create_response.status_code == 201
    created_budget = create_response.json()
    budget_id = created_budget["id"]

    # Now, update the budget entry
    updated_budget_data = {
        "amount": "600.00",
        "end_date": (datetime.utcnow() + timedelta(days=60)).isoformat()
    }

    update_response = client.put(f"/budgets/{budget_id}/?user_id={user_id}", json=updated_budget_data)

    assert update_response.status_code == 200
    updated_budget = update_response.json()
    assert updated_budget["amount"] == "600.00"
    assert updated_budget["end_date"] == updated_budget_data["end_date"]
    assert updated_budget["user_id"] == user_id

def test_get_all_budgets():
    response = client.get("/budgets/?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_budget():
    # Create a budget to delete
    budget_data = {
        "category": "food",
        "amount": "500.00",
        "start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
    user_id = 1

    create_response = client.post(f"/budgets/?user_id={user_id}", json=budget_data)
    assert create_response.status_code == 201
    budget_id = create_response.json()["id"]

    # Delete the budget
    response = client.delete(f"/budgets/{budget_id}/")
    assert response.status_code == 204

# Unit Test Cases
def test_add_budget():
    db = TestingSessionLocal()
    budget_data = Budget(
        user_id=1,
        category="health",
        amount=Decimal("1000.00"),
        start_date=datetime.utcnow() - timedelta(days=10),
        end_date=datetime.utcnow() + timedelta(days=20),
        current_usage=Decimal("0.00"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(budget_data)
    db.commit()
    db.refresh(budget_data)
    assert budget_data.id is not None
    assert budget_data.amount == Decimal("1000.00")
    db.close()

def test_search_budget_unit():
    db = TestingSessionLocal()
    budgets = db.query(Budget).filter(Budget.category == "health").all()
    assert len(budgets) >= 0
    db.close()
