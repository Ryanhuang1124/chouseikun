from fastapi import APIRouter
from uuid import uuid4
from pydantic import BaseModel, UUID4

router = APIRouter(
    prefix="/creator",
    tags=["creator"]
)

class ResponseCreator(BaseModel):
    msg: str
    creator_id: UUID4

@router.post("/init", response_model=ResponseCreator)
async def init_creator():
    new_id = uuid4()
    return ResponseCreator(msg="Creator ID generated", creator_id=new_id)
