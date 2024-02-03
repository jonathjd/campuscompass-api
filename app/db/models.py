from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


class School(Base):
    __tablename__ = "schools"
    unitid = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    # relationships
    locations = relationship("Location", back_populates="school")
    finances = relationship("Finance", back_populates="school")
    controls = relationship("Control", back_populates="school")
    admissions = relationship("Admission", back_populates="school")


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    school_unitid = Column(Integer, ForeignKey("schools.unitid"))
    city = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    state = Column(String, nullable=False)
    region = Column(String, nullable=False)
    locale = Column(String, nullable=True)

    # Relationship with School
    school = relationship("School", back_populates="locations")


class Finance(Base):
    __tablename__ = "finance"
    id = Column(Integer, primary_key=True)
    school_unitid = Column(Integer, ForeignKey("schools.unitid"))
    year = Column(Date)
    cost_attendance = Column(Float)
    avg_net_price = Column(Float)
    in_state_tuition = Column(Float)
    out_state_tuition = Column(Float)
    tuition_per_fte = Column(Float)
    instructional_expenditure_per_fte = Column(Float)
    avg_faculty_salary = Column(Float)

    # Relationship with School
    school = relationship("School", back_populates="finances")


class Control(Base):
    __tablename__ = "control"
    id = Column(Integer, primary_key=True)
    school_unitid = Column(Integer, ForeignKey("schools.unitid"))
    under_investigation = Column(Boolean)
    predominant_deg = Column(String)
    highest_deg = Column(String)
    control = Column(String)
    hbcu = Column(Boolean)
    religious_affiliation = Column(String)
    carnegie_undergrad = Column(String)
    carnegie_size = Column(String)

    # Relationship with School
    school = relationship("School", back_populates="controls")


class Admission(Base):
    __tablename__ = "admission"
    id = Column(Integer, primary_key=True)
    school_unitid = Column(Integer, ForeignKey("schools.unitid"))
    year = Column(Date)
    admission_rate = Column(Float)
    number_of_students = Column(Integer)
    sat_math_median = Column(Float)
    sat_reading_median = Column(Float)
    sat_writing_median = Column(Float)
    act_math_median = Column(Float)
    act_english_median = Column(Float)
    act_writing_median = Column(Float)
    act_cumulative_median = Column(Float)
    avg_sat_score_admitted = Column(Float)

    # Relationship with School
    school = relationship("School", back_populates="admissions")
