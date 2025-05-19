from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from typing import List
import uuid
from database import get_db
from models import Applicant, AvailableTime
from schemas import ApplicantUpdate

router = APIRouter(
    prefix='/applicant',
    tags=['applicant']
)

class AvailableTimeCreate(BaseModel):
    time_option_id: int

class ApplicantCreate(BaseModel):
    event_id: int
    available_times: List[AvailableTimeCreate]

class AvailableTimeRead(BaseModel):
    time_option_id: int

class ApplicantRead(BaseModel):
    id: str
    event_id: int
    updated_at: datetime
    available_times: List[AvailableTimeRead]

    model_config = {"from_attributes": True}


@router.post("/create", response_model=ApplicantRead)
def create_applicant(applicant: ApplicantCreate, db: Session = Depends(get_db)):
    new_applicant = Applicant(
        id=str(uuid.uuid4()),
        event_id=applicant.event_id,
    )
    db.add(new_applicant)
    db.flush()

    for time in applicant.available_times:
        db.add(AvailableTime(
            applicant_id=new_applicant.id,
            time_option_id=time.time_option_id
        ))

    db.commit()
    db.refresh(new_applicant)
    return new_applicant

@router.patch("/edit/{applicant_id}", response_model=ApplicantRead)
def update_applicant(
    applicant_id: str,
    update_data: ApplicantUpdate,
    db: Session = Depends(get_db),
):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    db.query(AvailableTime).filter(AvailableTime.applicant_id == applicant_id).delete()

    for time in update_data.available_times:
        db.add(AvailableTime(
            applicant_id=applicant_id,
            time_option_id=time.time_option_id
        ))

    applicant.updated_at = datetime.now()
    db.commit()
    db.refresh(applicant)

    return applicant

@router.delete("/delete/{applicant_id}")
def delete_applicant(applicant_id: str, db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    db.query(AvailableTime).filter(AvailableTime.applicant_id == applicant_id).delete()

    db.delete(applicant)
    db.commit()

    return {"msg": "Applicant deleted", "applicant_id": applicant_id}
