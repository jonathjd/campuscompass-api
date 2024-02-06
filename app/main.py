from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Depends, Request, Query
from app.db.database import SessionLocal
from app.db import models
from app.schemas.schemas import Header, SchoolSearchResponse, SchoolBase
from sqlalchemy.orm import Session, joinedload
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from functools import lru_cache
from . import settings


def get_db():
    """Context manager to ensure database connection is closed after request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()


@lru_cache
def get_settings():
    return settings.Settings()


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
    "/v1/schools/", status_code=status.HTTP_200_OK, response_model=SchoolSearchResponse
)
@limiter.limit("5/minute")
def get_schools_by_name(
    request: Request,
    school_name: str | None = Query(
        None, description="The partial or full name of the school to search for."
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, gt=0, le=1000),
    db: Session = Depends(get_db),
) -> SchoolSearchResponse:
    """
    Retrieves a list of schools matching the given search criteria with support for pagination.
    This endpoint is rate-limited to 5 requests per minute per user to ensure fair usage.

    The search is performed case-insensitively on the full or partial school name provided.
    Use the `skip` and `limit` query parameters to navigate through the results for large data sets.

    Args:
    - school_name (str, optional): The partial or full name of the school to search for. Defaults to None.
    - skip (int): The number of records to skip before starting to collect the response set. Defaults to 0.
    - limit (int): The maximum number of records to return. Defaults to 100 but can be adjusted as needed.

    Returns:
    SchoolSearchResponse: A JSON object with two main components:
    - `header`: Contains metadata such as the total number of matching records, the number of records skipped, and the limit applied.
    - `results`: A list of schools matching the search criteria. Each school includes basic information and a unique identifier.

    Example Input:
    GET /v1/schools/?school_name=California&skip=0&limit=10

    Note:
    - Exceeding the rate limit will result in a 429 status code.
    - An empty `results` list indicates no schools were found matching the criteria.
    - For best performance, it is recommended to keep the `limit` value reasonable, especially for broad searches.
    """
    query = db.query(models.School)
    if school_name:
        school_name_pattern = f"%{school_name.lower()}%"
        query = query.filter(models.School.name.ilike(school_name_pattern))

    total = query.count()
    schools = query.offset(skip).limit(limit).all()
    results = [models.School.from_orm(school) for school in schools]

    header = Header(total=total, skip=skip, limit=limit)
    return SchoolSearchResponse(header=header, results=results)


@app.get(
    "/v1/schools/state/",
    status_code=status.HTTP_200_OK,
    response_model=SchoolSearchResponse,
)
@limiter.limit("5/minute")
def get_school_by_state(
    request: Request,
    state_name: str | None = Query(
        None, description="The state to get all schools from."
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, gt=0, le=1000),
    db: Session = Depends(get_db),
) -> SchoolSearchResponse:
    """
    Retrieves a list of schools matching the given state with support for pagination.
    This endpoint is rate-limited to 5 requests per minute per user to ensure fair usage.

    The search is performed case-insensitively on the full or partial school name provided.
    Use the `skip` and `limit` query parameters to navigate through the results for large data sets.

    Args:
    - state_name (str, optional): The partial or full name of the school to search for. Defaults to None.
    - skip (int): The number of records to skip before starting to collect the response set. Defaults to 0.
    - limit (int): The maximum number of records to return. Defaults to 100 but can be adjusted as needed.

    Returns:
    SchoolSearchResponse: A JSON object with two main components:
    - `header`: Contains metadata such as the total number of matching records, the number of records skipped, and the limit applied.
    - `results`: A list of schools matching the search criteria along with location information

    Example Input:
    GET /v1/schools/state/?state_name=California&skip=0&limit=10

    Note:
    - Exceeding the rate limit will result in a 429 status code.
    - An empty `results` list indicates no schools were found matching the criteria.
    - For best performance, it is recommended to keep the `limit` value reasonable, especially for broad searches.
    """
    query = db.query(models.School).join(
        models.School, models.Location.school_unitid == models.School.unitid
    )
    if state_name:
        state_name = f"%{state_name.lower()}%"
        query = query.filter(models.Location.state.ilike(state_name)).options(
            joinedload(models.Location)
        )

    total = query.count()
    schools = query.offset(skip).limit(limit).all()

    results = []
    for school in schools:
        school_data = SchoolBase(
            unitid=school.unitid,
            name=school.name,
            url=school.url,
            location=school.location,
        )
        results.append(school_data)

    header = Header(total=total, skip=skip, limit=limit)
    return SchoolSearchResponse(header=header, results=results)
