from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from typing import List
import uuid
from database import get_db
from models import Applicant, AvailableTime
from schemas import ApplicantCreate, ApplicantRead, ApplicantUpdate

router = APIRouter(
    prefix='/applicant',
    tags=['applicant']
)


@router.post("/create", response_model=ApplicantRead)
def create_applicant(applicant: ApplicantCreate, db: Session = Depends(get_db)):
    new_applicant = Applicant(
        event_id=applicant.event_id,
    )
    db.add(new_applicant)
    db.flush()
    available_time_objects = []

    for time_option_id in applicant.available_times:
        available_time = AvailableTime(
            applicant_id=new_applicant.id,
            time_option_id=time_option_id
        )
        db.add(available_time)
        available_time_objects.append(available_time)

    db.commit()
    new_applicant.available_times = available_time_objects
    
    return new_applicant

@router.patch("/edit/{applicant_id}", response_model=ApplicantRead)
def update_applicant(
    applicant_id: int,
    update_data: ApplicantUpdate,
    db: Session = Depends(get_db),
):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    db.query(AvailableTime).filter(AvailableTime.applicant_id == applicant_id).delete()

    for time_option_id in update_data.available_times:
        db.add(AvailableTime(
            applicant_id=applicant_id,
            time_option_id=time_option_id
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
