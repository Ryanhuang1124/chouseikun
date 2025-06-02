from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from typing import List
from database import get_db
from models import Applicant, AvailableTime, Event, TimeOption
from schemas import ApplicantCreate, ApplicantRead, ApplicantUpdate

router = APIRouter(
    prefix='/applicant',
    tags=['applicant']
)

def validate_available_times(event_id: int, available_times: List[int], db: Session):
    """驗證傳入的 available_times 是否都屬於指定的 event"""
    # 獲取該 event 的所有 time_option_ids
    valid_time_option_ids = db.query(TimeOption.id).filter(TimeOption.event_id == event_id).all()
    valid_time_option_ids = [option.id for option in valid_time_option_ids]
    
    # 檢查是否有無效的 time_option_id
    invalid_time_options = [time_id for time_id in available_times if time_id not in valid_time_option_ids]
    
    if invalid_time_options:
        raise HTTPException(
            status_code=422, 
            detail=f"データの不整合：時間オプション {invalid_time_options} はこのイベントに属していません"
        )

@router.post("/create", response_model=ApplicantRead)
def create_applicant(applicant: ApplicantCreate, db: Session = Depends(get_db)):
    # 驗證 event 是否存在
    event = db.query(Event).filter(Event.id == applicant.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="イベントが見つかりません")
    
    # 驗證 available_times 是否都屬於該 event
    validate_available_times(applicant.event_id, applicant.available_times, db)
    
    new_applicant = Applicant(
        event_id=applicant.event_id,
        name=applicant.name,
        memo=applicant.memo,
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
        raise HTTPException(status_code=404, detail="申請者が見つかりません")
    
    # 驗證 available_times 是否都屬於該 applicant 的 event
    validate_available_times(applicant.event_id, update_data.available_times, db)
    
    if update_data.memo is not None:
        applicant.memo = update_data.memo

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
        raise HTTPException(status_code=404, detail="申請者が見つかりません")

    db.query(AvailableTime).filter(AvailableTime.applicant_id == applicant_id).delete()

    db.delete(applicant)
    db.commit()

    return {"msg": "Applicant deleted", "applicant_id": applicant_id}
