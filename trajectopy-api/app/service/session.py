import logging
import uuid
from datetime import datetime

from app.dependencies import get_storage
from app.dtos import SessionDTO
from app.exceptions import SessionAlreadyExistsException, SessionNotFoundException
from app.repository.models import Session
from app.repository.session import SessionRepository
from app.storage import StorageProtocol
from fastapi import Depends

logger = logging.getLogger("root")


class SessionService:

    def __init__(
        self,
        session_repository: SessionRepository = Depends(SessionRepository),
        storage: StorageProtocol = Depends(get_storage),
    ):
        self.session_repository = session_repository
        self.storage = storage

    def create_session(self, name: str | None = None) -> SessionDTO:
        session_id = uuid.uuid4().hex
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = name or f"Session {date}"

        if self.session_repository.get_session(session_id) is not None:
            raise SessionAlreadyExistsException()

        db_session = Session(**SessionDTO(id=session_id, date=date, name=name).model_dump())
        self.session_repository.create_session(db_session)
        self.storage.create_session(session_id=session_id)

        return SessionDTO.model_validate(db_session)

    def delete_session(self, session_id: str) -> None:
        if self.session_repository.get_session(session_id) is None:
            raise SessionNotFoundException(session_id)

        self.session_repository.delete_session(session_id)
        self.storage.delete_session(session_id=session_id)

    def get_sessions(self) -> list[SessionDTO]:
        return [SessionDTO.model_validate(s) for s in self.session_repository.get_all_sessions()]
