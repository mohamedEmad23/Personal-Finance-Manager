from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .core.database import SessionLocal, Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)


def cors_middleware_factory(app: FastAPI) -> CORSMiddleware:
    return CORSMiddleware(
        app=app,
        allow_origins=["*"],  # Replace with your desired origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to your personal financial tracker"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
