from database import Base
from sqlalchemy import UUID, ForeignKey,Column,Integer,String,Boolean,DateTime
from datetime import datetime
import uuid


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    memo = Column(String)
    selected_date = Column(DateTime,)
    user = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, default="anonymous")
