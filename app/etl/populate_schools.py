import logging
from college_scorecard_api import get_college_data
from app.db.models import School, Base
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


load_dotenv()

# db
try:
    DATABASE_URI = os.getenv("DATABASE_URI")
    engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
except SQLAlchemyError as e:
    logging.error("Database error: %s", e)
    exit(1)

# College Scorecard API setup
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    logging.error("Missing API key. Check your .env file.")
    exit(1)

fields = ["id", "school.name", "school.school_url"]

try:
    data = get_college_data(api_key=API_KEY, fields=fields, page_limit=3)
    logging.info("Data fetched from College Scorecard API.")
except Exception as e:
    logging.error("Error fetching data from API: %s", e)
    exit(1)

# Insert data into the database
session = Session()
try:
    for school_data in zip(data["id"], data["school.name"], data["school.school_url"]):
        unitid, name, url = school_data
        school = School(unitid=unitid, name=name, url=url)
        session.add(school)
    session.commit()
    logging.info("Data successfully inserted into the database.")
except SQLAlchemyError as e:
    session.rollback()
    logging.error("Error inserting data into the database: %s", e)
finally:
    session.close()
    logging.info("Database session closed.")
