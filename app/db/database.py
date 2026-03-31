import os
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
safe_password = quote_plus(DB_PASSWORD)

# 1. Check if the certificate actually exists
CA_PATH_OBJ = Path(__file__).resolve().parent / "certs" / "ca.pem"
CA_PATH = str(CA_PATH_OBJ.as_posix())

connect_args = {}

# 2. Only add SSL if the file is physically there
if CA_PATH_OBJ.exists():
    connect_args["ssl"] = {"ca": CA_PATH}
    print("Connecting with SSL (Aiven Mode)")
else:
    print("Connecting without SSL (Local/CI Mode)")


connect_args = {
    "ssl": {
        "ca": CA_PATH,
        "check_hostname": False  # This prevents some common Windows/Aiven mismatches
    },
    "connect_timeout": 60,       # Give it a full minute to connect
    "read_timeout": 60
}

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Create the engine with the dynamic connect_args
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fix: Define Base ONLY ONCE. 
# Defining it twice creates two different registries, which breaks migrations.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()