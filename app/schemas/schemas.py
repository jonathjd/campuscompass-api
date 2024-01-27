from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import datetime


class SchoolBase(BaseModel):
    unitid: int
    name: str
    url: HttpUrl | None = None


class SchoolCreate(SchoolBase):
    pass


class School(SchoolBase):
    id: int
    locations: List["Location"] = []
    finances: List["Finance"] = []
    controls: List["Control"] = []
    admissions: List["Admission"] = []

    class Config:
        orm_mode = True


class LocationBase(BaseModel):
    school_id: int
    city: str
    zipcode: str
    state: str
    region: str | None = None
    locale: str | None = None


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True


class FinanceBase(BaseModel):
    school_id: int
    year: datetime.date
    cost_attendance: float
    avg_net_price: float | None = None
    in_state_tuition: float
    out_state_tuition: float | None = None
    tuition_per_fte: float | None = None
    instructional_expenditure_per_fte: float | None = None
    avg_faculty_salary: float | None = None


class Finance(FinanceBase):
    id: int

    class Config:
        orm_mode = True


class ControlBase(BaseModel):
    school_id: int
    under_investigation: bool | None = None
    predominant_deg: str
    highest_deg: str
    control: str
    hbcu: bool | None = None
    religious_affiliation: str | None = None
    carnegie_undergrad: str
    carnegie_size: str


class Control(ControlBase):
    id: int

    class Config:
        orm_mode = True


class AdmissionBase(BaseModel):
    school_id: int
    year: datetime.date
    admission_rate: float
    number_of_students: int | None = None
    sat_math_median: float | None = None
    sat_reading_median: float | None = None
    sat_writing_median: float | None = None
    act_math_median: float | None = None
    act_english_median: float | None = None
    act_writing_median: float | None = None
    act_cumulative_median: float
    avg_sat_score_admitted: float


class Admission(AdmissionBase):
    id: int

    class Config:
        orm_mode = True
