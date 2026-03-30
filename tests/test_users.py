from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.db.test_database import TestingSessionLocal, engine
from app.models.user import Base
import pytest

client = TestClient(app)

# Create tables in TEST DB
Base.metadata.create_all(bind=engine)

# Override DB

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# Clean DB before each test
@pytest.fixture(autouse=True)
def clean_db():
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


# ---------------- TEST CASES ----------------

def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)