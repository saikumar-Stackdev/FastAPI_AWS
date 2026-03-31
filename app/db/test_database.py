import os
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Load env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
TEST_DB_NAME = os.getenv("TEST_DB_NAME") # Make sure this exists in Aiven!

safe_password = quote_plus(DB_PASSWORD)

# 2. Path to the SAME cert you used for the main DB
BASE_DIR = Path(__file__).resolve().parent
CA_PATH = (BASE_DIR / "certs" / "ca.pem").as_posix()

# 3. Connection URL
TEST_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)

# 4. Engine with SSL
# This matches your working main database configuration
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": CA_PATH
        }
    },
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()