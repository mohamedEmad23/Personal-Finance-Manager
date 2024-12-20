import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..core.database import Base, get_db
from ..main import app
from ..models.income import Income
from ..schemas.incomeSchema import IncomeFrequency

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
def test_create_income():
    income_data = {
        "amount": 1000.0,
        "description": "Monthly Salary",
        "frequency": "monthly",
        "source": "Salary"
    }
    user_id = 1

    response = client.post(f"/incomes/?user_id={user_id}", json=income_data)

    assert response.status_code == 201
    created_income = response.json()
    assert created_income["amount"] == 1000.0
    assert created_income["description"] == "Monthly Salary"
    assert created_income["frequency"] == "monthly"
    assert created_income["source"] == "Salary"
    assert created_income["user_id"] == user_id

def test_update_income():
    # First, create an income entry to update
    income_data = {
        "amount": 1000.0,
        "description": "Monthly Salary",
        "frequency": "monthly",
        "source": "Salary"
    }
    user_id = 1

    create_response = client.post(f"/incomes/?user_id={user_id}", json=income_data)

    assert create_response.status_code == 201
    created_income = create_response.json()
    income_id = created_income["id"]

    # Now, update the income entry
    updated_income_data = {
        "amount": 1200.0,
        "description": "Updated Monthly Salary",
        "frequency": "monthly",
        "source": "Updated Salary"
    }

    update_response = client.put(f"/incomes/{income_id}/?user_id={user_id}", json=updated_income_data)

    assert update_response.status_code == 200
    updated_income = update_response.json()
    assert updated_income["amount"] == 1200.0
    assert updated_income["description"] == "Updated Monthly Salary"
    assert updated_income["frequency"] == "monthly"
    assert updated_income["source"] == "Updated Salary"
    assert updated_income["user_id"] == user_id

def test_get_all_incomes():
    response = client.get("/income/incomes?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_income():
    # Create an income to delete
    income_data = {
        "amount": 1000.0,
        "description": "Monthly Salary",
        "frequency": "monthly",
        "source": "Salary"
    }
    user_id = 1

    create_response = client.post(f"/incomes/?user_id={user_id}", json=income_data)
    assert create_response.status_code == 201
    income_id = create_response.json()["id"]

    # Delete the income
    response = client.delete(f"/incomes/{income_id}/")
    assert response.status_code == 204

def test_search_incomes():
    response = client.get("/incomes/search/?frequency=monthly&user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Unit Test Cases
def test_add_income():
    db = TestingSessionLocal()
    income_data = Income(
        user_id=1,
        amount=500.00,
        description="Part-time Job",
        frequency=IncomeFrequency.DAILY,
        source="Job",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(income_data)
    db.commit()
    db.refresh(income_data)
    assert income_data.id is not None
    assert income_data.amount == 500.00
    db.close()

def test_search_income_unit():
    db = TestingSessionLocal()
    incomes = db.query(Income).filter(Income.frequency == IncomeFrequency.DAILY).all()
    assert len(incomes) >= 0
    db.close()
