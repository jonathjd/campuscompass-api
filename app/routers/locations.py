from fastapi import APIRouter, status, Depends, Request, Query
from app.db import models
from app.schemas.schemas import Header, SchoolSearchResponse, SchoolBase
from sqlalchemy.orm import Session, joinedload
from app.dependencies.dependencies import limiter, get_db

router = APIRouter(prefix="/v1/schools", tags=["locations"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=SchoolSearchResponse)
@limiter.limit("5/minute")
def get_schools_by_name(
    request: Request,
    school_name: str = Query(
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
    query = db.query(models.School).filter(
        models.School.name.ilike(f"%{school_name.lower()}%")
    )

    total = query.count()
    schools = query.offset(skip).limit(limit).all()
    results = [models.School.from_orm(school) for school in schools]

    header = Header(total=total, skip=skip, limit=limit)
    return SchoolSearchResponse(header=header, results=results)


@router.get(
    "/state/",
    status_code=status.HTTP_200_OK,
    response_model=SchoolSearchResponse,
)
@limiter.limit("5/minute")
def get_school_by_state(
    request: Request,
    state_name: str = Query(None, description="The state to get all schools from."),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, gt=0, le=1000),
    db: Session = Depends(get_db),
) -> SchoolSearchResponse:
    """
    Retrieves a list of schools matching the given state with support for pagination.
    This endpoint is rate-limited to 5 requests per minute per user to ensure fair usage.

    The search is performed case-insensitively on the full or partial state provided.
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
    query = (
        db.query(models.School)
        .join(models.School, models.Location.school_unitid == models.School.unitid)
        .filter(models.Location.state.ilike(f"%{state_name.lower()}%"))
        .options(joinedload(models.Location))
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


@router.get(
    "/region/",
    status_code=status.HTTP_200_OK,
    response_model=SchoolSearchResponse,
)
@limiter.limit("5/minute")
def get_school_by_region(
    request: Request,
    region: str = Query(None, description="The region to get all schools from."),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, gt=0, le=1000),
    db: Session = Depends(get_db),
) -> SchoolSearchResponse:
    """
    Retrieves a list of schools matching a given region with support for pagination.
    This endpoint is rate-limited to 5 requests per minute per user to ensure fair usage.

    The search is performed case-insensitively on the full or partial region provided.
    Use the `skip` and `limit` query parameters to navigate through the results for large data sets.

    Available regions:
    - U.S. Service Schools
    - New England (CT, ME, MA, NH, RI, VT)
    - Mid East (DE, DC, MD, NJ, NY, PA)
    - Great Lakes (IL, IN, MI, OH, WI)
    - Plains (IA, KS, MN, MO, NE, ND, SD)
    - Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)
    - Southwest (AZ, NM, OK, TX)
    - Rocky Mountains (CO, ID, MT, UT, WY)
    - Far West (AK, CA, HI, NV, OR, WA)
    - Outlying Areas (AS, FM, GU, MH, MP, PR, PW, VI)

    `Consequently, passing a state code will result in all schools in that region being returned`

    Args:
    - state_name (str, optional): The partial or full name of the state to query. Defaults to None.
    - skip (int): The number of records to skip before starting to collect the response set. Defaults to 0.
    - limit (int): The maximum number of records to return. Defaults to 100 but can be adjusted as needed.

    Returns:
    SchoolSearchResponse: A JSON object with two main components:
    - `header`: Contains metadata such as the total number of matching records, the number of records skipped, and the limit applied.
    - `results`: A list of schools matching the search criteria along with location information

    Example Input:
    GET /v1/schools/region/?region=Southeast&skip=0&limit=10

    Note:
    - Exceeding the rate limit will result in a 429 status code.
    - An empty `results` list indicates no schools were found matching the criteria.
    - For best performance, it is recommended to keep the `limit` value reasonable, especially for broad searches.
    """

    query = (
        db.query(models.School)
        .join(models.School, models.Location.school_unitid == models.School.unitid)
        .filter(models.location.region.ilike(f"%{region.lower()}%"))
        .options(joinedload(models.Location))
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


@router.get(
    "/locale/",
    status_code=status.HTTP_200_OK,
    response_model=SchoolSearchResponse,
)
@limiter.limit("5/minute")
def get_school_by_locale(
    request: Request,
    locale: str = Query(None, description="The locale to get all schools from."),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, gt=0, le=1000),
    db: Session = Depends(get_db),
) -> SchoolSearchResponse:
    """
    Retrieves a list of schools matching a given locale with support for pagination.
    This endpoint is rate-limited to 5 requests per minute per user to ensure fair usage.

    The search is performed case-insensitively on the full or partial locale provided.

    Available locales:
    - City
    - Suburb
    - Town
    - Rural

    Args:
    - state_name (str, optional): The partial or full name of the locale to query. Defaults to None.
    - skip (int): The number of records to skip before starting to collect the response set. Defaults to 0.
    - limit (int): The maximum number of records to return. Defaults to 100 but can be adjusted as needed.

    Returns:
    SchoolSearchResponse: A JSON object with two main components:
    - `header`: Contains metadata such as the total number of matching records, the number of records skipped, and the limit applied.
    - `results`: A list of schools matching the search criteria along with location information

    Example Input:
    GET /v1/schools/locale/?locale=City&skip=0&limit=10

    Note:
    - Exceeding the rate limit will result in a 429 status code.
    - An empty `results` list indicates no schools were found matching the criteria.
    - For best performance, it is recommended to keep the `limit` value reasonable, especially for broad searches.
    """

    query = (
        db.query(models.School)
        .join(models.School, models.Location.school_unitid == models.School.unitid)
        .filter(models.location.locale.ilike(f"%{locale.lower()}%"))
        .options(joinedload(models.Location))
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


@router.get(
    "/zipcode/",
    status_code=status.HTTP_200_OK,
    response_model=SchoolSearchResponse,
)
@limiter.limit("5/minute")
def get_school_by_zip(
    request: Request,
    zipcode: str = Query(None, description="The zipcode to get all schools from."),
    skip: int | None = Query(default=0, ge=0),
    limit: int | None = Query(default=100, gt=0, le=1000),
    db: Session = Depends(get_db),
) -> SchoolSearchResponse:
    """
    Retrieves a list of schools matching a given zipcode with support for pagination.
    This endpoint is rate-limited to 5 requests per minute per user to ensure fair usage.

    Args:
    - zipcode (str): The partial or full name of the locale to query. Defaults to None.
    - skip (int): The number of records to skip before starting to collect the response set. Defaults to 0.
    - limit (int): The maximum number of records to return. Defaults to 100 but can be adjusted as needed.

    Returns:
    SchoolSearchResponse: A JSON object with two main components:
    - `header`: Contains metadata such as the total number of matching records, the number of records skipped, and the limit applied.
    - `results`: A list of schools matching the search criteria along with location information

    Example Input:
    GET /v1/schools/zipcode/?zipcode=98926&skip=0&limit=10

    Note:
    - Exceeding the rate limit will result in a 429 status code.
    - An empty `results` list indicates no schools were found matching the criteria.
    - For best performance, it is recommended to keep the `limit` value reasonable, especially for broad searches.
    """

    query = (
        db.query(models.School)
        .join(models.School, models.Location.school_unitid == models.School.unitid)
        .filter(models.location.locale.ilike(zipcode))
        .options(joinedload(models.Location))
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
