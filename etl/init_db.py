from sqlalchemy import create_engine
from db_model import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.environ.get("DATABASE_URI")


def initialize_database():
    engine = create_engine(DATABASE_URI)

    Base.metadata.create_all(engine)
    print("Database tables created")


if __name__ == "__main__":
    initialize_database()
