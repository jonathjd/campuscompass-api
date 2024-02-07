from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from functools import lru_cache
from app import settings
from app.routers import locations
from app.dependencies.dependencies import limiter


@lru_cache
def get_settings():
    return settings.Settings()


config = get_settings()

app = FastAPI(title=config.app_name)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    """Health check route."""
    return {"health_check": "OK"}


app.include_router(locations.router)
