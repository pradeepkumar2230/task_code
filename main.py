from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from infrastructure import schemas, database, models
from infrastructure.database import get_db

app = FastAPI(
    title="Medication Management API",
    description="API for managing patient medication requests",
    version="1.0.0"
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def read_root():
    return {"message": "Medication Management API"}


@app.post("/patients/{patient_id}/medication-requests",
          response_model=schemas.MedicationRequestResponse)
def create_medication_request(
        patient_id: int,
        request: schemas.MedicationRequestCreate,
        db: Session = Depends(get_db)
):
    """Create a new medication request for a patient"""

    # Verify patient exists
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Verify clinician exists
    clinician = db.query(models.Clinician).filter(
        models.Clinician.id == request.clinician_id
    ).first()
    if not clinician:
        raise HTTPException(status_code=404, detail="Clinician not found")

    # Verify medication exists
    medication = db.query(models.Medication).filter(
        models.Medication.id == request.medication_id
    ).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")

    # Create medication request
    db_request = models.MedicationRequest(
        patient_id=patient_id,
        **request.dict()
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return db_request


@app.get("/patients/{patient_id}/medication-requests",
         response_model=List[schemas.MedicationRequestResponse])
def get_medication_requests(
        patient_id: int,
        status: Optional[str] = Query(None, description="Filter by status"),
        prescribed_from: Optional[date] = Query(None, description="Filter from prescribed date"),
        prescribed_to: Optional[date] = Query(None, description="Filter to prescribed date"),
        db: Session = Depends(get_db)
):
    """Get medication requests for a patient with optional filtering"""

    # Verify patient exists
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Build query
    query = db.query(models.MedicationRequest).filter(
        models.MedicationRequest.patient_id == patient_id
    )

    # Apply filters
    if status:
        query = query.filter(models.MedicationRequest.status == status)

    if prescribed_from:
        query = query.filter(models.MedicationRequest.prescribed_date >= prescribed_from)

    if prescribed_to:
        query = query.filter(models.MedicationRequest.prescribed_date <= prescribed_to)

    return query.all()


@app.patch("/patients/{patient_id}/medication-requests/{request_id}",
           response_model=schemas.MedicationRequestResponse)
def update_medication_request(
        patient_id: int,
        request_id: int,
        update_data: schemas.MedicationRequestUpdate,
        db: Session = Depends(get_db)
):
    """Update specific fields of a medication request"""

    # Find the medication request
    db_request = db.query(models.MedicationRequest).filter(
        models.MedicationRequest.id == request_id,
        models.MedicationRequest.patient_id == patient_id
    ).first()

    if not db_request:
        raise HTTPException(status_code=404, detail="Medication request not found")

    # Update only provided fields
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(db_request, field, value)

    db.commit()
    db.refresh(db_request)

    return db_request
