from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends, HTTPException
from app.db import models, SessionLocal
from schemas import schemas
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to ensure database connection is closed after request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(lifespan=lifespan)
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
def home():
    """Health check route."""
    return {"health_check": "OK"}


@app.get(
    "/v1/schools/{unitid}",
    response_model=schemas.School,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
def get_school_by_unitid(unitid: int, db: Session = Depends(lifespan)):
    """
    Retrieve a school by its unit ID with rate limiting.

    Args:
    - unitid (int): The unique identifier for the school.
    - db (Session, optional): Database session dependency.

    Returns:
    - dict: The school information or an error message.
    """
    db_school = db.query(models.School).filter(models.School.unitid == unitid).first()
    if db_school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="School not found"
        )
    return db_school


@app.get(
    "/v1/schools/{school_name}",
    response_model=List[schemas.School],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
def get_schools_by_name(
    school_name: str,
    db: Session = Depends(lifespan),
    skip: int | None = 0,
    limit: int | None = 100,
) -> List[schemas.School]:
    """
    Retrieve a list of schools by name with pagination and rate limiting.

    Args:
    - school_name (str): The name or partial name to search for.
    - db (Session, optional): Database session dependency.
    - skip (int, optional): Number of records to skip for pagination.
    - limit (int, optional): Maximum number of records to return.

    Returns:
    - List[schemas.School]: A list of schools matching the search criteria.
    """
    school_name_pattern = school_name.lower() + "%"
    schools = (
        db.query(models.School)
        .filter(models.School.name.ilike(school_name_pattern))
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not schools:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schools not found"
        )
    return schools
