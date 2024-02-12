import logging
from college_scorecard_api import get_college_data
from app.db.models import Location
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from utils.data_cleaning import transform_zipcode

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


def main():
    try:
        TEST_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
        engine = create_engine(TEST_DATABASE_URI)
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

    try:
        data = get_college_data(api_key=API_KEY, fields=fields, page_limit=2)
        logging.info("Data fetched from College Scorecard API.")
    except Exception as e:
        logging.error("Error fetching data from API: %s", e)
        exit(1)

    # Insert data into the database
    session = Session()
    try:
        region_ids = {
            0: "U.S. Service Schools",
            1: "New England (CT, ME, MA, NH, RI, VT)",
            2: "Mid East (DE, DC, MD, NJ, NY, PA)",
            3: "Great Lakes (IL, IN, MI, OH, WI)",
            4: "Plains (IA, KS, MN, MO, NE, ND, SD)",
            5: "Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)",
            6: "Southwest (AZ, NM, OK, TX)",
            7: "Rocky Mountains (CO, ID, MT, UT, WY)",
            8: "Far West (AK, CA, HI, NV, OR, WA)",
            9: "Outlying Areas (AS, FM, GU, MH, MP, PR, PW, VI)",
        }

        locale_ids = {
            11: "City: Large (population of 250,000 or more)",
            12: "City: Midsize (population of at least 100,000 but less than 250,000)",
            13: "City: Small (population less than 100,000)",
            21: "Suburb: Large (outside principal city, in urbanized area with population of 250,000 or more)",
            22: "Suburb: Midsize (outside principal city, in urbanized area with population of at least 100,000 but less than 250,000)",
            23: "Suburb: Small (outside principal city, in urbanized area with population less than 100,000)",
            31: "Town: Fringe (in urban cluster up to 10 miles from an urbanized area)",
            32: "Town: Distant (in urban cluster more than 10 miles and up to 35 miles from an urbanized area)",
            33: "Town: Remote (in urban cluster more than 35 miles from an urbanized area)",
            41: "Rural: Fringe (rural territory up to 5 miles from an urbanized area or up to 2.5 miles from an urban cluster)",
            42: "Rural: Distant (rural territory more than 5 miles but up to 25 miles from an urbanized area or more than 2.5 and up to 10 miles from an urban cluster)",
            43: "Rural: Remote (rural territory more than 25 miles from an urbanized area and more than 10 miles from an urban cluster)",
        }

        for location in zip(
            data["id"],
            data["school.city"],
            data["school.state"],
            data["school.zip"],
            data["school.region_id"],
            data["school.locale"],
        ):
            unitid = location[0]
            city = location[1]
            state = location[2]
            zipcode = transform_zipcode(location[3])

            region_number = location[4]
            region_id = region_ids[region_number]

            locale_number = location[5]

            try:
                locale_id = locale_ids[locale_number]

            except:
                locale_id = "None"

            location_insert = Location(
                school_unitid=unitid,
                state=state,
                city=city,
                zipcode=zipcode,
                region=region_id,
                locale=locale_id,
            )

            session.add(location_insert)
        session.commit()
        logging.info("Data successfully inserted into the database.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error("Error inserting data into the database: %s", e)
    finally:
        session.close()
        logging.info("Database session closed.")


if __name__ == "__main__":
    main()
