import os
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Load environment variables SAFELY
# This prevents FileNotFoundError on GitHub
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") or "" # Fallback to empty string for safety
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
safe_password = quote_plus(DB_PASSWORD)

# 2. Setup SSL Path Logic
BASE_DIR = Path(__file__).resolve().parent
CA_PATH_OBJ = BASE_DIR / "certs" / "ca.pem"

# Initialize empty connect_args
connect_args = {
    "connect_timeout": 60,
    "read_timeout": 60
}

# 3. Only add SSL if the file is physically there
if CA_PATH_OBJ.exists():
    connect_args["ssl"] = {
        "ca": str(CA_PATH_OBJ.as_posix()),
        "check_hostname": False
    }
    print("--- Connecting with SSL (Aiven Mode) ---")
else:
    print("--- Connecting WITHOUT SSL (Local/GitHub Mode) ---")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 4. Create the engine
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()