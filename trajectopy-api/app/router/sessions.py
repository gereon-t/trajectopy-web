import logging

from app.dtos import SessionDTO
from app.service.session import SessionService
from fastapi import APIRouter, Depends

logger = logging.getLogger("root")

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/create", status_code=201)
async def create_sesssion_endpoint(
    name: str | None = None,
    session_service: SessionService = Depends(SessionService),
) -> SessionDTO:
    return session_service.create_session(name)


@router.delete("/delete", status_code=204)
async def delete_session_endpoint(session_id: str, session_service: SessionService = Depends(SessionService)) -> None:
    session_service.delete_session(session_id)


@router.get("/", status_code=200)
async def get_sessions_endpoint(session_service: SessionService = Depends(SessionService)) -> list[SessionDTO]:
    return session_service.get_sessions()
