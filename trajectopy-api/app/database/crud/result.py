import uuid

from sqlalchemy.orm import Session

from app.database import models
from app.database.schemas import result as result_schemas
from app.storage.storage_protocol import StorageProtocol


def add_result(
    db: Session,
    storage: StorageProtocol,
    session_id: str,
    result: result_schemas.ResultBaseSchema,
    report: str,
) -> models.Result:
    db_result = create_result(db, result, session_id=session_id)
    storage.write_result(session_id=session_id, result_id=db_result.id, result=report)
    return db_result


def create_result(
    db: Session, result: result_schemas.ResultBaseSchema, session_id: str
):
    db_result = models.Result(
        **result.model_dump(),
        id=uuid.uuid4().hex,
        session_id=session_id,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_result(db: Session, result_id: str):
    return db.query(models.Result).filter(models.Result.id == result_id).first()


def delete_result(db: Session, result_id: str):
    db.query(models.Result).filter_by(id=result_id).delete()
    db.commit()
