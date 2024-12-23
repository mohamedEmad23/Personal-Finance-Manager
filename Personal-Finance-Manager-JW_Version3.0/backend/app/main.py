import os
from dotenv import load_dotenv

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends, HTTPException

from .api.notifications import notification_router
from .api.users import router as users_router
from .api.budgets import budget_router
from .api.reports import report_router
from .core.database import SessionLocal, Base, engine
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .api.expenses import expense_router
from .api.income import income_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Mount static directory for plots
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(expense_router, prefix="/api/v1/expenses", tags=["expenses"])
app.include_router(income_router, prefix="/api/v1/income", tags=["income"])
app.include_router(budget_router, prefix="/api/v1/budgets", tags=["budgets"])
app.include_router(report_router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(notification_router, prefix="/api/v1/notifications", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": "Welcome to your personal financial tracker"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Load environment variables from the .env file
load_dotenv()

# Get the SMTP_PORT from the environment variables
smtp_port = os.getenv("SMTP_PORT")

# Print the SMTP_PORT to the console
print(f"SMTP Port: {smtp_port}")
