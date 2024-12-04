from fastapi import FastAPI, Depends, HTTPException
from app.api.users import router as users_router
from .api.budgets import budget_router
from .api.reports import report_router
from .core.database import SessionLocal, Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.expenses import expense_router
from app.api.income import income_router
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(users_router, tags=["users"])
app.include_router(auth_router,  tags=["auth"])
app.include_router(expense_router,  tags=["expenses"])
app.include_router(income_router, tags=["income"])
app.include_router(budget_router,  tags=["budgets"])
app.include_router(report_router,  tags=["reports"])


def cors_middleware_factory(app: FastAPI) -> CORSMiddleware:
    return CORSMiddleware(
        app=app,
        allow_origins=["*"],  # Replace with your desired origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    return {"message": "Welcome to your personal financial tracker"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

