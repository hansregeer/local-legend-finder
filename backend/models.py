from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    strava_id = Column(Integer, unique=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    activities = relationship("Activity", back_populates="user")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    strava_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    distance = Column(Float)
    moving_time = Column(Integer)
    activity_type = Column(String)
    start_date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")
