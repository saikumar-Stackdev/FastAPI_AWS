import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

def get_test_engine():
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")  # safe fallback
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("TEST_DB_NAME", "fastapi_test_db")

    safe_password = quote_plus(str(db_password))

    url = f"mysql+pymysql://{db_user}:{safe_password}@{db_host}:{db_port}/{db_name}"

    return create_engine(url)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_test_engine()
)