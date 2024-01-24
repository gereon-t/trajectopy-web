import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database import models
from app.database.crud import session as session_crud
from app.storage.protocol import Storage

logger = logging.getLogger("root")

SESSION_TIMEOUT = timedelta(days=1)


def is_session_expired(session: models.Session) -> bool:
    return (
        datetime.now() - datetime.strptime(session.date, "%Y-%m-%d %H:%M:%S")
    ) > SESSION_TIMEOUT


def check_expired_sessions(db: Session, storage: Storage):
    for session in session_crud.get_all_sessions(db):
        if is_session_expired(session):
            logger.info("Session %s expired", session.id)
            session_crud.delete_session(db, session.id)
            storage.delete_session(session_id=session.id)
