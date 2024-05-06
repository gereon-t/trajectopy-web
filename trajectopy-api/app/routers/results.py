from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.crud import result as result_crud
from app.database.schemas import result as result_schemas
from app.dependencies import get_db, get_storage
from app.storage.storage_protocol import StorageProtocol

router = APIRouter()


@router.delete("/results/{result_id}")
async def delete_result_endpoint(
    result_id: str,
    db: Session = Depends(get_db),
    storage: StorageProtocol = Depends(get_storage),
):
    result = result_crud.get_result(db, result_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")

    try:
        storage.remove_result(session_id=result.session_id, result_id=result.id)
        result_crud.delete_result(db, result.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return Response(status_code=204)


@router.get("/results/{result_id}", response_model=result_schemas.ResultSchema)
async def get_result_endpoint(result_id: str, db: Session = Depends(get_db)):
    result = result_crud.get_result(db, result_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")

    return result


@router.get("/results/render/{result_id}")
async def render_result_endpoint(
    result_id: str,
    db: Session = Depends(get_db),
    storage: StorageProtocol = Depends(get_storage),
):
    result = result_crud.get_result(db, result_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")

    try:
        report = storage.read_result(result.session_id, result.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return Response(report, media_type="text/html")
