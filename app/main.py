import requests
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.models import Base, engine, SessionLocal

Base.metadata.create_engine_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"health_check": "OK"}
