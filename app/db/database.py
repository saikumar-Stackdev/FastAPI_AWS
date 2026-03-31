import os
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Load .env only if it exists
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# 2. Get Variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") or ""
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
safe_password = quote_plus(DB_PASSWORD)

# 3. SSL Logic - THE CRITICAL PART
BASE_DIR = Path(__file__).resolve().parent
CA_PATH_OBJ = BASE_DIR / "certs" / "ca.pem"

# Start with basic timeouts
connect_args = {
    "connect_timeout": 60,
    "read_timeout": 60
}

# ONLY add the "ssl" key if the file is physically present
if CA_PATH_OBJ.exists():
    # We use str() and as_posix() for Windows compatibility
    connect_args["ssl"] = {
        "ca": str(CA_PATH_OBJ.as_posix()),
        "check_hostname": False
    }
    print("SSL enabled for Aiven connection.")
else:
    # If the file is missing (like on GitHub), we DON'T add the "ssl" key at all
    print("SSL disabled. Using standard connection.")

# 4. Create Engine
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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