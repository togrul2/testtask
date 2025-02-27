"""
This script creates the tables in the database.
It drops all existing tables and creates new ones.
It should be run only once at the beginning of the project and is meant for testing purposes.
Migration tools must be used for production databases.
"""

import models  # noqa: F401
from database import engine, Base


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
