from sqlalchemy.orm import Session
from db import models
from schemas import schemas


def get_school_by_unitid(db: Session, unit_id: int):
    return db.query(models.School).filter(models.School.unitid == unit_id).first()


def get_school_by_name(db: Session, school_name: str):
    return db.query(models.School).filter(models.School.name == school_name).first()


def get_schools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.School).offset(limit).all()
