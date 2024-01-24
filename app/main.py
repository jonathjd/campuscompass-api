import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def home():
    return {"health_check": "OK"}
