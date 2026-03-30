import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

def get_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD") or ""
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT") or "3306"
    db_name = os.getenv("DB_NAME")

    safe_password = quote_plus(str(db_password))

    DATABASE_URL = f"mysql+pymysql://{db_user}:{safe_password}@{db_host}:{db_port}/{db_name}"

    return create_engine(DATABASE_URL)


def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

def get_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD") or ""
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT") or "3306"
    db_name = os.getenv("DB_NAME")

    safe_password = quote_plus(str(db_password))

    DATABASE_URL = f"mysql+pymysql://{db_user}:{safe_password}@{db_host}:{db_port}/{db_name}"

    return create_engine(DATABASE_URL)


def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())