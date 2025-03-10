import logging

from app.dependencies import get_db
from app.repository import models
from fastapi import Depends
from sqlalchemy.orm import Session

logger = logging.getLogger("root")


class SessionRepository:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_session(self, session: models.Session) -> models.Session:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_all_sessions(self) -> list[models.Session]:
        return self.db.query(models.Session).all()

    def get_session(self, session_id: str) -> models.Session | None:
        return self.db.query(models.Session).filter(models.Session.id == session_id).first()

    def delete_session(self, session_id: str) -> None:
        self.db.query(models.Session).filter_by(id=session_id).delete()

        for trajectory in self.db.query(models.Trajectory).filter_by(session_id=session_id):
            self.db.query(models.Trajectory).filter_by(id=trajectory.id).delete()

        for result in self.db.query(models.Result).filter_by(session_id=session_id):
            self.db.query(models.Result).filter_by(id=result.id).delete()

        self.db.commit()
