from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
from .config import settings

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

if "sslmode" not in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = DATABASE_URL
# urllib.parse.quote_plus("@")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                password='Waveysxn@2025', cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print("Database connection was succesfull!")
#        break
#    except Exception as error:
#        print("Connection to the database failed!")
#        print("Error: ", error)
#        time.sleep(3)
