from database import Base
from sqlalchemy import UUID, ForeignKey,Column,Integer,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    memo = Column(String)
    user = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    time_options = relationship("TimeOption", back_populates="event", cascade="all, delete")

class TimeOption(Base):
    __tablename__ = "time_options"
    id = Column(Integer, primary_key=True)
    label = Column(String)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="time_options")


class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    available_times = relationship("AvailableTime", backref="applicant", cascade="all, delete-orphan")


class AvailableTime(Base):
    __tablename__ = "available_times"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(String, ForeignKey("applicants.id"), nullable=False)
    time_option_id = Column(Integer, ForeignKey("time_options.id"), nullable=False)
