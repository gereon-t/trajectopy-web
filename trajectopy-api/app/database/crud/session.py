import logging

from sqlalchemy.orm import Session

from app.database import models
from app.database.schemas import session as session_schemas

logger = logging.getLogger("root")


def create_session(db: Session, session: session_schemas.SessionBaseSchema):
    db_session = models.Session(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_all_sessions(db: Session) -> list[models.Session]:
    return db.query(models.Session).all()


def get_session(db: Session, session_id: str):
    return db.query(models.Session).filter(models.Session.id == session_id).first()


def delete_session(db: Session, session_id: str):
    db.query(models.Session).filter_by(id=session_id).delete()
    db.commit()

    for trajectory in db.query(models.Trajectory).filter_by(session_id=session_id):
        db.query(models.Result).filter_by(trajectory_id=trajectory.id).delete()
        db.query(models.Trajectory).filter_by(id=trajectory.id).delete()

    db.commit()
