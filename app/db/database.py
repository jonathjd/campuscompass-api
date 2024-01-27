from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.environ.get("DATABASE_URI")

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
