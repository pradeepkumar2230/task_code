from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Date, ForeignKey, Enum as SqlEnum
from datetime import date
import enum
from typing import Optional


class Base(DeclarativeBase):
    pass


class SexEnum(str, enum.Enum):
    male = "male"
    female = "female"


class FormEnum(str, enum.Enum):
    powder = "powder"
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"


class StatusEnum(str, enum.Enum):
    active = "active"
    on_hold = "on-hold"
    cancelled = "cancelled"
    completed = "completed"


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[SexEnum] = mapped_column(SqlEnum(SexEnum), nullable=False)

    medication_requests: Mapped[list["MedicationRequest"]] = relationship(
        back_populates="patient"
    )


class Clinician(Base):
    __tablename__ = "clinicians"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    registration_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    medication_requests: Mapped[list["MedicationRequest"]] = relationship(
        back_populates="clinician"
    )


class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    code_name: Mapped[str] = mapped_column(String, nullable=False)
    code_system: Mapped[str] = mapped_column(String, nullable=False)
    strength_value: Mapped[float] = mapped_column(Float, nullable=False)
    strength_unit: Mapped[str] = mapped_column(String, nullable=False)
    form: Mapped[FormEnum] = mapped_column(SqlEnum(FormEnum), nullable=False)

    medication_requests: Mapped[list["MedicationRequest"]] = relationship(
        back_populates="medication"
    )


class MedicationRequest(Base):
    __tablename__ = "medication_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    clinician_id: Mapped[int] = mapped_column(ForeignKey("clinicians.id"), nullable=False)
    medication_id: Mapped[int] = mapped_column(ForeignKey("medications.id"), nullable=False)
    reason_text: Mapped[str] = mapped_column(String)
    prescribed_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    frequency: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    patient: Mapped["Patient"] = relationship(back_populates="medication_requests")
    clinician: Mapped["Clinician"] = relationship(back_populates="medication_requests")
    medication: Mapped["Medication"] = relationship(back_populates="medication_requests")
