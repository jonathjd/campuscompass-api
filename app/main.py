import requests
from fastapi import FastAPI
from sqlalchemy import create_engine
from app.db.models import Base
import os

app = FastAPI()


@app.on_event("startup")
async def startup():
    print("Starting up...")
    DATABASE_URI = os.environ.get("DATABASE_URI")
    print(f"Database URI: {DATABASE_URI}")

    try:
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)
        print("Database tables created")
    except Exception as e:
        print(f"Error during startup: {e}")


@app.get("/")
def home():
    return {"health_check": "OK"}
