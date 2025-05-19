from pydantic import BaseModel
from typing import List


class TimeOptionSchema(BaseModel):
    label: str
    model_config = {
    "from_attributes": True
}

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


class ResponseEventList(BaseModel):
    msg: str
    count: int
    event_list: List[dict]

class AvailableTimeRead(BaseModel):
    id: int
    applicant_id: str
    time_option_id: int
    model_config = {
        "from_attributes": True
    }

class ApplicantRead(BaseModel):
    id: str
    event_id: int
    available_times: List[AvailableTimeRead] = []
    model_config = {
        "from_attributes": True
    }
class AvailableTimeCreate(BaseModel):
    time_option_id: int

class ApplicantUpdate(BaseModel):
    id: str
    event_id: int
    available_times: List[AvailableTimeCreate]
