from sqlalchemy.orm import Session
from db import models
from schemas import schemas


def get_school_by_unitid(db: Session, unit_id: int):
    """
    retrieve a school by its unique identifier (unitid).

    :param db: sqlalchemy session for database access
    :param unit_id: unique identifier of the school
    :return: first school record matching the given unit_id or None if no match is found
    """
    return db.query(models.School).filter(models.School.unitid == unit_id).first()


def get_school_by_name(db: Session, school_name: str):
    """
    retrieve a school by its name.

    :param db: sqlalchemy session for database access
    :param school_name: name of the school to find
    :return: first school record matching the given name or None if no match is found
    """
    return db.query(models.School).filter(models.School.name == school_name).first()


def get_schools(db: Session, skip: int = 0, limit: int = 100):
    """
    retrieve a list of schools, with pagination.

    :param db: sqlalchemy session for database access
    :param skip: number of records to skip for pagination
    :param limit: maximum number of records to return
    :return: list of schools based on pagination parameters
    """
    return db.query(models.School).offset(skip).limit(limit).all()
