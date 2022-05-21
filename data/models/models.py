from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, nullable=False)
    group_id = Column(Integer)
    name = Column(String(50))


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    group_name = Column(String(50), nullable=False)


class Workouts(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    workout_type = Column(String(50), nullable=False)
    distance = Column(Float, nullable=False)
    workout_name = Column(String(100))
    elapsed_time = Column(Integer, nullable=False)
    workout_date = Column(DateTime, nullable=False)


class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    access_token = Column(String(100))
    refresh_token = Column(String(100))
    expires_in = Column(Integer)
    expires_at = Column(Integer)
    updated_at = Column(DateTime, onupdate=datetime.now(), default=datetime.now())
