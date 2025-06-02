import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from main import app
from infrastructure.database import get_db
from infrastructure.models import Base, Patient, Clinician, Medication, SexEnum, FormEnum

# Dynamic DB URL fallback
DB_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def setup_test_data():
    db = TestingSessionLocal()

    # Clear tables before each test
    db.query(Medication).delete()
    db.query(Clinician).delete()
    db.query(Patient).delete()
    db.commit()

    patient = Patient(
        first_name="Ram",
        last_name="Kumar",
        date_of_birth=date(1990, 1, 1),
        sex=SexEnum.male
    )
    db.add(patient)

    clinician = Clinician(
        first_name="Dr. Jane",
        last_name="Smith",
        registration_id="REG123"
    )
    db.add(clinician)

    medication = Medication(
        code="747006",
        code_name="Oxamniquine",
        code_system="SNOMED",
        strength_value=5.0,
        strength_unit="g/ml",
        form=FormEnum.tablet
    )
    db.add(medication)

    db.commit()
    db.refresh(patient)
    db.refresh(clinician)
    db.refresh(medication)

    yield {
        "patient_id": patient.id,
        "clinician_id": clinician.id,
        "medication_id": medication.id
    }

    db.close()


def test_create_medication_request(setup_test_data):
    test_data = setup_test_data

    request_data = {
        "clinician_id": test_data["clinician_id"],
        "medication_id": test_data["medication_id"],
        "reason_text": "Infection treatment",
        "prescribed_date": "2025-05-15",
        "start_date": "2025-05-16",
        "frequency": "3 times/day",
        "status": "active"
    }

    response = client.post(
        f"/patients/{test_data['patient_id']}/medication-requests",
        json=request_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reason_text"] == "Infection treatment"
    assert data["status"] == "active"


def test_get_medication_requests(setup_test_data):
    # First create a request
    test_data = setup_test_data

    request_data = {
        "clinician_id": test_data["clinician_id"],
        "medication_id": test_data["medication_id"],
        "prescribed_date": "2025-05-15",
        "start_date": "2025-05-16",
        "status": "active"
    }

    client.post(
        f"/patients/{test_data['patient_id']}/medication-requests",
        json=request_data
    )

    # Then get requests
    response = client.get(f"/patients/{test_data['patient_id']}/medication-requests")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["status"] == "active"


def test_update_medication_request(setup_test_data):
    # First create a request
    test_data = setup_test_data

    request_data = {
        "clinician_id": test_data["clinician_id"],
        "medication_id": test_data["medication_id"],
        "prescribed_date": "2025-05-15",
        "start_date": "2025-05-16",
        "status": "active"
    }

    create_response = client.post(
        f"/patients/{test_data['patient_id']}/medication-requests",
        json=request_data
    )

    request_id = create_response.json()["id"]

    # Update the request
    update_data = {
        "status": "completed",
        "end_date": "2025-05-30"
    }

    response = client.patch(
        f"/patients/{test_data['patient_id']}/medication-requests/{request_id}",
        json=update_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["end_date"] == "2025-05-30"
