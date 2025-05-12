from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from starlette import status

from models import Users
from database import DB_ANNOTATED

router = APIRouter(
    prefix='/user',
    tags=['user']
)

class RequestUsers(BaseModel):
    class Config:
        json_schema_extra={
			'example':{
			'name':"Ryan",
			}
		}

class ResponseUsers(BaseModel):
    msg : str
    user_id : int

class ResponseUsersList(BaseModel):
    msg : str
    user_list : list
    count : int

@router.get("/",status_code=status.HTTP_200_OK,response_model=ResponseUsersList)
async def get_all_user(session:DB_ANNOTATED):
    
    data = [{'user_id': user.id} for user in session.query(Users).all()]

    return ResponseUsersList(msg="success",count= len(data),user_list=data)

@router.post("/register" ,status_code=status.HTTP_201_CREATED,response_model=ResponseUsers)
async def create_user(session:DB_ANNOTATED, request_data : RequestUsers):
    data = Users()
        
    user = session.query(Users).filter( Users.account == data.account ).first()

    if not user:
        session.add(data)
        session.commit()
        return ResponseUsers(msg='User Created',user_id=data.id)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists.")
