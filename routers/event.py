from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from models import Event, Users
from database import DB_ANNOTATED
from datetime import datetime

router = APIRouter(
    prefix='/event',
    tags=['event']
)

class RequestEvent(BaseModel):
    title: str
    memo: str = ""
    selected_date: datetime
    user: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "カラオケ",
                "memo": "一緒に歌おう",
                "selected_date": "2025-05-20T15:00:00",
                "user": "Ryan"
            }
        }

class ResponseEvent(BaseModel):
    msg: str
    event_id: int

class ResponseEventList(BaseModel):
    msg: str
    count: int
    event_list: list

@router.post("/create", response_model=ResponseEvent, status_code=status.HTTP_201_CREATED)
async def create_event(session: DB_ANNOTATED, request_data: RequestEvent):
    event = Event(
        title=request_data.title,
        memo=request_data.memo,
        selected_date=request_data.selected_date,
        user=request_data.user
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return ResponseEvent(msg="Event created", event_id=event.id)

@router.get("/", response_model=ResponseEventList, status_code=status.HTTP_200_OK)
async def get_all_events(session: DB_ANNOTATED):
    events = session.query(Event).all()
    result = [
        {
            "id": e.id,
            "title": e.title,
            "memo": e.memo,
            "selected_date": e.selected_date,
            "user": e.user,
            "created_at": e.created_at
        }
        for e in events
    ]
    return ResponseEventList(msg="success", count=len(result), event_list=result)

@router.get("/by-user/{user_name}", response_model=ResponseEventList, status_code=status.HTTP_200_OK)
async def get_events_by_user(user_name: str, session: DB_ANNOTATED):
    events = session.query(Event).filter(Event.user == user_name).all()
    result = [
        {
            "id": e.id,
            "title": e.title,
            "memo": e.memo,
            "selected_date": e.selected_date,
            "user": e.user,
            "created_at": e.created_at
        }
        for e in events
    ]
    return ResponseEventList(msg="success", count=len(result), event_list=result)
