from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")

engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if DATABASE_URI.startswith("sqlite:"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
