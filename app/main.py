from fastapi import FastAPI
from app.db.database import Base, engine
from app.routes import user

app = FastAPI()

# DEV ONLY
Base.metadata.create_all(bind=engine)

app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "CRUD API running"}