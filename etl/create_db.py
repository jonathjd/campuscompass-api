from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unitid = Column(Integer, unique=True)
    url = Column(String)

    # relationships
    locations = relationship("Location", back_populates="school")
    finances = relationship("Finance", back_populates="school")
    controls = relationship("Control", back_populates="school")
    admissions = relationship("Admission", back_populates="school")


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    city = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    state = Column(String, nullable=False)
    region = Column(String, nullable=False)
    locale = Column(String)

    # Relationship with School
    school = relationship("School", back_populates="locations")


class Finance(Base):
    __tablename__ = "finance"
    id = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    year = Column(Date)
    cost_attendance = Column(Float)
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
    school_id = Column(Integer, ForeignKey("schools.id"))
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
    school_id = Column(Integer, ForeignKey("schools.id"))
    year = Column(Date)
    admission_rate = Column(Float)
    sat_math_median = Column(Float)
    sat_reading_median = Column(Float)
    sat_writing_median = Column(Float)
    act_math_median = Column(Float)
    act_english_median = Column(Float)
    act_writing_median = Column(Float)
    act_cumulative_median = Column(Float)

    # Relationship with School
    school = relationship("School", back_populates="admissions")
