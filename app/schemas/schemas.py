from pydantic import BaseModel, HttpUrl, ConfigDict, validator
from datetime import date


class Header(BaseModel):
    total: int
    skip: int
    limit: int


class LocationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    zipcode: str
    state: str
    region: str | None = None
    locale: str | None = None


class FinanceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    year: date
    cost_attendance: float
    avg_net_price: float | None = None
    in_state_tuition: float
    out_state_tuition: float | None = None
    tuition_per_fte: float | None = None
    instructional_expenditure_per_fte: float | None = None
    avg_faculty_salary: float | None = None


class ControlBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    under_investigation: bool | None = None
    predominant_deg: str
    highest_deg: str
    control: str
    hbcu: bool | None = None
    religious_affiliation: str | None = None
    carnegie_undergrad: str
    carnegie_size: str | None = None


class AdmissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    year: date
    admission_rate: float
    number_of_students: int | None = None
    sat_math_median: float | None = None
    sat_reading_median: float | None = None
    sat_writing_median: float | None = None
    act_math_median: float | None = None
    act_english_median: float | None = None
    act_writing_median: float | None = None
    act_cumulative_median: float
    avg_sat_score_admitted: float | None = None


class SchoolBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    unitid: int
    name: str
    url: HttpUrl | None = None
    location: LocationBase | None = None
    finances: list[FinanceBase] | None = None
    admissions: list[AdmissionBase] | None = None
    control: ControlBase | None = None

    @validator("url", pre=True, always=True)
    def ensure_url_scheme(cls, v):
        if v and not v.startswith(("http://", "https://")):
            return f"http://{v}"
        return v


class SchoolSearchResponse(BaseModel):
    header: Header
    results: list[SchoolBase]
