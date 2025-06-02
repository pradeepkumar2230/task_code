from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from infrastructure.models import SexEnum, FormEnum, StatusEnum


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: SexEnum


class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True


class ClinicianBase(BaseModel):
    first_name: str
    last_name: str
    registration_id: str


class Clinician(ClinicianBase):
    id: int

    class Config:
        from_attributes = True


class MedicationBase(BaseModel):
    code: str
    code_name: str
    code_system: str
    strength_value: float
    strength_unit: str
    form: FormEnum


class Medication(MedicationBase):
    id: int

    class Config:
        from_attributes = True


class MedicationRequestCreate(BaseModel):
    clinician_id: int
    medication_id: int
    reason_text: Optional[str] = None
    prescribed_date: date
    start_date: date
    end_date: Optional[date] = None
    frequency: Optional[str] = None
    status: StatusEnum = StatusEnum.active


class MedicationRequestUpdate(BaseModel):
    end_date: Optional[date] = None
    frequency: Optional[str] = None
    status: Optional[StatusEnum] = None


class MedicationRequestResponse(BaseModel):
    id: int
    patient_id: int
    clinician_id: int
    medication_id: int
    reason_text: Optional[str]
    prescribed_date: date
    start_date: date
    end_date: Optional[date]
    frequency: Optional[str]
    status: StatusEnum

    # Related data for response
    patient: Patient
    clinician: Clinician
    medication: Medication

    class Config:
        from_attributes = True