import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from database import Base
from models import Application as ApplicationModel


# Separate in-memory database for tests
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()

    db.query(ApplicationModel).delete()
    db.commit()
    db.close()

    yield


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API is running"
    }


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Test Company",
            "role": "Python Intern",
            "status": "Applied",
            "application_date": "2026-10-26",
            "job_link": "https://example.com",
            "notes": "Automated test"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Test Company"
    assert data["role"] == "Python Intern"
    assert data["status"] == "Applied"


def test_get_applications():
    response = client.get("/applications")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_update_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Test Company",
            "role": "Python Intern",
            "status": "Applied",
            "application_date": "2026-10-26",
            "job_link": "https://example.com",
            "notes": "Test application"
        }
    )

    application_id = create_response.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        json={
            "company": "Google",
            "role": "AI Engineer Intern",
            "status": "Interview",
            "application_date": "2026-10-26",
            "job_link": "https://google.com",
            "notes": "Interview scheduled"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Google"
    assert data["status"] == "Interview"


def test_delete_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Delete Test",
            "role": "Python Intern",
            "status": "Applied",
            "application_date": "2026-10-26",
            "job_link": "https://example.com",
            "notes": "Delete test"
        }
    )

    application_id = create_response.json()["id"]

    response = client.delete(
        f"/applications/{application_id}"
    )

    assert response.status_code == 200


def test_invalid_application():
    response = client.post(
        "/applications",
        json={
            "company": "",
            "role": "Python Intern",
            "status": "Applied",
            "application_date": "2026-10-26",
            "job_link": "hello",
            "notes": "Invalid test"
        }
    )

    assert response.status_code == 422