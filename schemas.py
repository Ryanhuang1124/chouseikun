from datetime import datetime
from pydantic import BaseModel
from typing import List


class TimeOptionSchema(BaseModel):
    label: str
    model_config = {
    "from_attributes": True
}
    
class TimeOptionIdOnly(BaseModel):
    time_option_id: int

class ApplicantCreate(BaseModel):
    event_id: int
    available_times: List[int]
    name:str
    memo:str
    

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": 1,
                "available_times": [1, 2],
                "name": "山田太郎",
                "memo": "よろしくお願いします"
            }
        }
    }

class TimeOptionRead(BaseModel):
    id: int
    label: str

    model_config = {"from_attributes": True}

class RequestEvent(BaseModel):
    title: str
    memo: str = ""
    user: str
    time_options: List[TimeOptionSchema]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "カラオケ",
                "memo": "一緒に歌おう",
                "user": "fbef1ca6-4479-42b1-97bc-06c611d617ca",
                "time_options": [
                    {"label": "5月20日午後"},
                    {"label": "5月22日夜間"}
                ]
            }
        }


class ResponseEvent(BaseModel):
    msg: str
    event_id: int


class ResponseEventDetail(BaseModel):
    msg: str   
    id: int
    title: str
    memo: str
    user: str
    created_at: datetime
    time_options: List[TimeOptionRead]


class ResponseEventList(BaseModel):
    msg: str
    count: int
    event_list: List[dict]

class AvailableTimeRead(BaseModel):
    time_option_id: int
    model_config = {
        "from_attributes": True
    }

class ApplicantRead(BaseModel):
    id: int
    event_id: int
    available_times: List[AvailableTimeRead] = []
    model_config = {
        "from_attributes": True
    }
class AvailableTimeCreate(BaseModel):
    time_option_id: int

class ApplicantUpdate(BaseModel):
    available_times: List[int]
    model_config = {
        "json_schema_extra": {
            "example": {
                "available_times": [1, 2, 3]
            }
        }
    }
