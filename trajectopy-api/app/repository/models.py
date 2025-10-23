from app.repository import Base
from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    date = Column(String, index=True)
    name = Column(String)

    trajectories = relationship("Trajectory", back_populates="session")


class Trajectory(Base):
    __tablename__ = "trajectories"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    epsg = Column(Integer)
    duration = Column(String)
    datarate = Column(Integer)
    num_poses = Column(Integer)
    has_orientations = Column(Boolean)
    settings = Column(JSON)
    session_id = Column(String, ForeignKey("sessions.id"))

    session = relationship("Session", back_populates="trajectories")


class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    session_id = Column(String, ForeignKey("sessions.id"))
