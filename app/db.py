from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

PG_USER = os.environ.get("PG_USER")
PG_PASSWORD = os.environ.get("PG_PASSWORD")
PG_HOST = os.environ.get("PG_HOST")
PG_PORT = os.environ.get("PG_PORT")
PG_DBNAME = os.environ.get("PG_DBNAME")

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DBNAME
    )
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
session = SessionLocal()
