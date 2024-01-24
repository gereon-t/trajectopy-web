from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.crud import trajectory as trajectory_crud
from app.database.schemas import settings as settings_schemas
from app.dependencies import get_db

router = APIRouter()


@router.put("/settings/update")
async def update_settings_endpoint(
    trajectory_id: str,
    settings: settings_schemas.SettingsSchema,
    db: Session = Depends(get_db),
):
    db_trajectory = trajectory_crud.get_trajectory(db, trajectory_id)
    if db_trajectory is None:
        raise HTTPException(status_code=400, detail="Trajectory not found")

    try:
        trajectory_crud.update_settings(db, trajectory_id, settings)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return Response(f"Updated settings of trajectory {trajectory_id}", status_code=200)


@router.put("/settings/update/single")
async def update_single_settings_endpoint(
    trajectory_id: str, settings: dict, db: Session = Depends(get_db)
):
    db_trajectory = trajectory_crud.get_trajectory(db, trajectory_id)
    if db_trajectory is None:
        raise HTTPException(status_code=400, detail="Trajectory not found")

    try:
        trajectory_crud.update_single_settings(db, trajectory_id, settings)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return Response(f"Updated settings of trajectory {trajectory_id}", status_code=200)


@router.get(
    "/settings/{trajectory_id}",
    response_model=settings_schemas.SettingsSchema,
)
async def get_settings_endpoint(trajectory_id: str, db: Session = Depends(get_db)):
    db_trajectory = trajectory_crud.get_trajectory(db, trajectory_id)
    if db_trajectory is None:
        raise HTTPException(status_code=400, detail="Trajectory not found")

    try:
        return trajectory_crud.get_settings(db, trajectory_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
