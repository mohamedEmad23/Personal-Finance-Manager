from fastapi import FastAPI, Depends, HTTPException
from app.api.users import router as users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Remove the line that creates tables with SQLAlchemy since it's not needed for MongoDB

app.include_router(users_router)

# CORS middleware setup
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
