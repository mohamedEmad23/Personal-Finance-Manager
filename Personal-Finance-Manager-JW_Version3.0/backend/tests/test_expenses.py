import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..core.database import Base, get_db
from ..main import app
from ..models.expense import Expense
from ..schemas.expenseSchema import ExpenseCategory

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
    # Base.metadata.drop_all(bind=engine)

# Integration Test Cases
def test_create_expense():
    expense_data = {
        "amount": 200.0,
        "category": "food",
        "description": "Groceries",
        "date": "2024-12-20T10:00:00"
    }
    user_id = 1

    response = client.post(f"/expenses/?user_id={user_id}", json=expense_data)

    assert response.status_code == 201
    created_expense = response.json()
    assert created_expense["amount"] == 200.0
    assert created_expense["category"] == "food"
    assert created_expense["description"] == "Groceries"
    assert created_expense["user_id"] == user_id

def test_update_expense():
    # First, create an expense entry to update
    expense_data = {
        "amount": 200.0,
        "category": "food",
        "description": "Groceries",
        "date": "2024-12-20T10:00:00"
    }
    user_id = 1

    create_response = client.post(f"/expenses/?user_id={user_id}", json=expense_data)

    assert create_response.status_code == 201
    created_expense = create_response.json()
    expense_id = created_expense["id"]

    # Now, update the expense entry
    updated_expense_data = {
        "amount": 250.0,
        "category": "utilities",
        "description": "Electricity Bill",
        "date": "2024-12-21T10:00:00"
    }

    update_response = client.put(f"/expenses/{expense_id}/?user_id={user_id}", json=updated_expense_data)

    assert update_response.status_code == 200
    updated_expense = update_response.json()
    assert updated_expense["amount"] == 250.0
    assert updated_expense["category"] == "utilities"
    assert updated_expense["description"] == "Electricity Bill"
    assert updated_expense["user_id"] == user_id

def test_get_all_expenses():
    response = client.get("/expenses/?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_expense():
    # Create an expense to delete
    expense_data = {
        "amount": 200.0,
        "category": "food",
        "description": "Groceries",
        "date": "2024-12-20T10:00:00"
    }
    user_id = 1

    create_response = client.post(f"/expenses/?user_id={user_id}", json=expense_data)
    assert create_response.status_code == 201
    expense_id = create_response.json()["id"]

    # Delete the expense
    response = client.delete(f"/expenses/{expense_id}/")
    assert response.status_code == 204

def test_search_expenses():
    response = client.get("/expenses/search/?category=food&user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Unit Test Cases
def test_add_expense():
    db = TestingSessionLocal()
    expense_data = Expense(
        user_id=1,
        amount=300.00,
        category=ExpenseCategory.HEALTH,
        description="Medical Checkup",
        date=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(expense_data)
    db.commit()
    db.refresh(expense_data)
    assert expense_data.id is not None
    assert expense_data.amount == 300.00
    db.close()

def test_search_expense_unit():
    db = TestingSessionLocal()
    expenses = db.query(Expense).filter(Expense.category == ExpenseCategory.HEALTH).all()
    assert len(expenses) >= 0
    db.close()
