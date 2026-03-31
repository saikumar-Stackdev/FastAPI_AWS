import os
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Load env safely (won't crash if .env is missing on GitHub)
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# 2. Get Variables with Defaults for GitHub
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "test")

safe_password = quote_plus(DB_PASSWORD)

# 3. Dynamic SSL Logic
CA_PATH_OBJ = BASE_DIR / "certs" / "ca.pem"
connect_args = {"connect_timeout": 60}

# ONLY add SSL if the cert actually exists (Aiven mode)
if CA_PATH_OBJ.exists():
    connect_args["ssl"] = {
        "ca": str(CA_PATH_OBJ.as_posix()),
        "check_hostname": False
    }
    print("--- Test DB: SSL Enabled (Aiven) ---")
else:
    # This runs on GitHub! No 'ssl' key means no FileNotFoundError
    print("--- Test DB: SSL Disabled (CI/Local) ---")

# 4. Connection URL
TEST_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)

# 5. Create Engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()