import requests
from fastapi import FastAPI
from sqlalchemy import create_engine
from app.db.models import Base
import os

app = FastAPI()


@app.get("/")
def home():
    return {"health_check": "OK"}
