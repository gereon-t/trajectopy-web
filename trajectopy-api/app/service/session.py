import logging
import uuid
from datetime import datetime, timedelta

from app.dependencies import get_storage
from app.dtos import SessionDTO
from app.exceptions import (SessionAlreadyExistsException,
                            SessionNotFoundException)
from app.repository.models import Session
from app.repository.session import SessionRepository
from app.storage import StorageProtocol
from fastapi import Depends

logger = logging.getLogger("root")


SESSION_TIMEOUT = timedelta(days=1)


class SessionService:

    def __init__(
        self,
        session_repository: SessionRepository = Depends(SessionRepository),
        storage: StorageProtocol = Depends(get_storage),
    ):
        self.session_repository = session_repository
        self.storage = storage

    def create_session(self, custom_id: str | None = None) -> SessionDTO:
        session_id = custom_id or uuid.uuid4().hex
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.session_repository.get_session(session_id) is not None:
            raise SessionAlreadyExistsException()

        db_session = Session(**SessionDTO(id=session_id, date=date).model_dump())
        self.session_repository.create_session(db_session)
        self.storage.create_session(session_id=session_id)
        self.check_expired_sessions()

        return SessionDTO.model_validate(db_session)

    def delete_session(self, session_id: str) -> None:
        if self.session_repository.get_session(session_id) is None:
            raise SessionNotFoundException(session_id)

        self.session_repository.delete_session(session_id)
        self.storage.delete_session(session_id=session_id)

    def check_expired_sessions(self) -> None:
        for session in self.session_repository.get_all_sessions():
            if self.is_session_expired(session):
                logger.info("Session %s expired", session.id)
                self.session_repository.delete_session(session.id)
                self.storage.delete_session(session_id=session.id)

    def is_session_expired(self, session: Session) -> bool:
        return (datetime.now() - datetime.strptime(session.date, "%Y-%m-%d %H:%M:%S")) > SESSION_TIMEOUT
