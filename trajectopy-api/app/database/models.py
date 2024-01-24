from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    date = Column(String, index=True)

    trajectories = relationship("Trajectory", back_populates="session")


class Trajectory(Base):
    __tablename__ = "trajectories"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    epsg = Column(Integer, index=True)
    sorting = Column(String, index=True)
    settings = Column(JSON)
    session_id = Column(String, ForeignKey("sessions.id"))

    session = relationship("Session", back_populates="trajectories")


class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
