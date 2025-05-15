from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from sqlalchemy.orm import Session,joinedload
from starlette import status
from models import Applicant, Event, TimeOption
from database import DB_ANNOTATED, get_db
from typing import List

from schemas import ApplicantRead, RequestEvent, ResponseEvent, ResponseEventList

router = APIRouter(
    prefix='/event',
    tags=['event']
)



@router.post("/create", response_model=ResponseEvent, status_code=status.HTTP_201_CREATED)
async def create_event(session: DB_ANNOTATED, request_data: RequestEvent):
    event = Event(
        title=request_data.title,
        memo=request_data.memo,
        user=request_data.user
    )

    session.add(event)
    session.flush()

    for option in request_data.time_options:
        session.add(TimeOption(label=option.label, event_id=event.id))

    session.commit()
    session.refresh(event)

    return ResponseEvent(msg="Event created", event_id=event.id)


@router.get("/", response_model=ResponseEventList)
async def get_all_events(session: DB_ANNOTATED):
    events = session.query(Event).all()
    result = [
        {
            "id": e.id,
            "title": e.title,
            "memo": e.memo,
            "user": e.user,
            "created_at": e.created_at,
            "time_options": [t.label for t in e.time_options]
        }
        for e in events
    ]
    return ResponseEventList(msg="success", count=len(result), event_list=result)


@router.get("/by-user/{user_name}", response_model=ResponseEventList)
async def get_events_by_user(user_name: str, session: DB_ANNOTATED):
    events = session.query(Event).filter(Event.user == user_name).all()
    result = [
        {
            "id": e.id,
            "title": e.title,
            "memo": e.memo,
            "user": e.user,
            "created_at": e.created_at,
            "time_options": [t.label for t in e.time_options]
        }
        for e in events
    ]
    return ResponseEventList(msg="success", count=len(result), event_list=result)


@router.get("/{event_id}/applicants", response_model=List[ApplicantRead])
def get_applicants_by_event(event_id: int, db: Session = Depends(get_db)):
    applicants = (
        db.query(Applicant)
        .filter(Applicant.event_id == event_id)
        .options(joinedload(Applicant.available_times))
        .all()
    )
    return applicants