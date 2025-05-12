from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres.loylnhbshqtecebkneaj:dJkMdfB7RWKuqR8D@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres'

engine = create_engine( SQLALCHEMY_DATABASE_URL )
local_session = sessionmaker( autocommit=False, autoflush=False,bind = engine)
Base = declarative_base()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

DB_ANNOTATED = Annotated[Session,Depends(get_db)]