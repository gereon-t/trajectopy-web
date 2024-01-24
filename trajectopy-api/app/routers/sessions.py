import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.crud import session as session_crud
from app.database.schemas import session as session_schemas
from app.dependencies import get_db, get_storage
from app.expiration import check_expired_sessions
from app.storage.protocol import Storage

logger = logging.getLogger("root")

router = APIRouter()


@router.post("/sessions/create", response_model=session_schemas.SessionSchema)
async def create_sesssion_endpoint(
    custom_id: str | None = None,
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    session_id = custom_id or uuid.uuid4().hex
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if session_crud.get_session(db, session_id) is not None:
        raise HTTPException(status_code=400, detail="Session already exists")

    try:
        db_session = session_crud.create_session(
            db, session_schemas.SessionBaseSchema(id=session_id, date=date)
        )
        storage.create_session(session_id=session_id)
        check_expired_sessions(db, storage)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return db_session


@router.delete("/sessions/delete")
async def delete_session_endpoint(
    session_id: str,
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    if session_crud.get_session(db, session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        session_crud.delete_session(db, session_id)
        storage.delete_session(session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return Response(f"Session {session_id} deleted", status_code=200)
