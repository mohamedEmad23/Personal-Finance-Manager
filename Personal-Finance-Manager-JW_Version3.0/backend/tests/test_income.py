from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from datetime import datetime
from ..app.main import app
from ..app.core.database import Base, get_db

TEST_DATABASE_URL = "mysql://root:johnw126126@localhost/finance_manager_sp"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
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


def test_create_income():
    income_data = {
        "amount": 1000.0,
        "description": "Monthly Salary",
        "frequency": "monthly",
        "source": "Salary"
    }
    user_id = 1

    response = client.post(
        f"/incomes/?user_id={user_id}",
        json=income_data
    )

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

    create_response = client.post(
        f"/incomes/?user_id={user_id}",
        json=income_data
    )

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

    update_response = client.put(
        f"/incomes/{income_id}/?user_id={user_id}",
        json=updated_income_data
    )

    assert update_response.status_code == 200
    updated_income = update_response.json()
    assert updated_income["amount"] == 1200.0
    assert updated_income["description"] == "Updated Monthly Salary"
    assert updated_income["frequency"] == "monthly"
    assert updated_income["source"] == "Updated Salary"
    assert updated_income["user_id"] == user_id
