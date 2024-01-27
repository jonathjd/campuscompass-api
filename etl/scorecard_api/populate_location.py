import logging
from college_scorecard_api import get_college_data
from db.models.db_model import Location, Base
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()

# Database setup
try:
    DATABASE_URI = os.getenv("DATABASE_URI")
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
except SQLAlchemyError as e:
    logging.error("Database error: %s", e)
    exit(1)

# College Scorecard API setup
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    logging.error("Missing API key. Check your .env file.")
    exit(1)

fields = [
    "id",
    "school.city",
    "school.state",
    "school.zip",
    "school.region_id",
    "school.locale",
]


# __tablename__ = "location"
# id = Column(Integer, primary_key=True)
# school_id = Column(Integer, ForeignKey("schools.id"))
# city = Column(String, nullable=False)
# zipcode = Column(String, nullable=False)
# state = Column(String, nullable=False)
# region = Column(String, nullable=False)
# locale = Column(String)

try:
    data = get_college_data(api_key=API_KEY, fields=fields)
    logging.info("Data fetched from College Scorecard API.")
except Exception as e:
    logging.error("Error fetching data from API: %s", e)
    exit(1)

# Insert data into the database
session = Session()
try:
    for location_data in zip(
        data["school.city"],
        data["school.state"],
        data["school.zip"],
        data["school.region_id"],
        data["school.locale"],
    ):
        city, state, zipcode, region_id, locale = location_data
        location = Location(
            city=city,
            zipcode=zipcode,
            state=state,
            region=region_id,
            locale=locale,
        )
        session.add(location)
    session.commit()
    logging.info("Data successfully inserted into the database.")
except SQLAlchemyError as e:
    session.rollback()
    logging.error("Error inserting data into the database: %s", e)
finally:
    session.close()
    logging.info("Database session closed.")
