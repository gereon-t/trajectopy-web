import trajectopy_core.trajectory as tpy_trajectory
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from trajectopy_core.trajectory import Trajectory

from app.database.crud import result as result_crud
from app.database.crud import session as session_crud
from app.database.crud import trajectory as trajectory_crud
from app.database.schemas import result as result_schemas
from app.database.schemas import settings as settings_schemas
from app.database.schemas import trajectory as trajectory_schemas
from app.dependencies import (
    get_db,
    get_est_trajectory,
    get_gt_trajectory,
    get_storage,
    get_trajectories,
    get_trajectory,
)
from app.storage.protocol import Storage
from app.utils import create_comparison_report, create_plot_report

router = APIRouter()


@router.get("/trajectories/", response_model=list[trajectory_schemas.TrajectorySchema])
async def get_trajectories_endpoint(session_id: str, db: Session = Depends(get_db)):
    trajectories = trajectory_crud.get_trajectories(db, session_id)

    if trajectories is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return trajectories


@router.get(
    "/trajectories/{trajectory_id}", response_model=trajectory_schemas.TrajectorySchema
)
async def get_trajectory_endpoint(trajectory_id: str, db: Session = Depends(get_db)):
    trajectory = trajectory_crud.get_trajectory(db, trajectory_id)

    if not trajectory:
        raise HTTPException(status_code=404, detail="Trajectory not found")

    return trajectory


@router.post("/trajectories/upload", response_model=trajectory_schemas.TrajectorySchema)
async def upload_trajectory_endpoint(
    session_id: str,
    file: UploadFile,
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    if session_crud.get_session(db, session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found")

    input_stream = str(file.file.read(), encoding="utf-8")

    try:
        read_trajectory = tpy_trajectory.Trajectory.from_file(
            input_stream, io_stream=True
        )
        db_trajectory = trajectory_crud.add_trajectory(
            db, storage, read_trajectory, session_id
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return db_trajectory


@router.delete("/trajectories/{trajectory_id}")
async def delete_trajectory_endpoint(
    trajectory_id: str,
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    trajectory = trajectory_crud.get_trajectory(db, trajectory_id)

    if trajectory is None:
        raise HTTPException(status_code=404, detail="Trajectory not found")

    try:
        trajectory_crud.delete_trajectory(db, trajectory_id)
        storage.remove_trajectory(
            session_id=trajectory.session_id, trajectory_id=trajectory_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return Response(f"Trajectory {trajectory_id} deleted", status_code=200)


@router.get("/trajectories/download/{trajectory_id}")
async def download_trajectory_endpoint(
    trajectory: Trajectory = Depends(get_trajectory),
):
    if trajectory is None:
        raise HTTPException(status_code=404, detail="Trajectory not found")

    try:
        csv_data = str(trajectory.to_dataframe().to_csv(index=False))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return PlainTextResponse(csv_data, media_type="text/csv")


@router.post("/trajectories/compare", response_model=result_schemas.ResultSchema)
async def compare_trajectories_endpoint(
    session_id: str,
    gt_trajectory: Trajectory = Depends(get_gt_trajectory),
    est_trajectory: Trajectory = Depends(get_est_trajectory),
    settings: settings_schemas.SettingsSchema = settings_schemas.SettingsSchema(),
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    if not gt_trajectory or not est_trajectory:
        raise HTTPException(status_code=404, detail="Trajectory not found")

    try:
        report = create_comparison_report(
            gt_traj=gt_trajectory, est_traj=est_trajectory, settings=settings
        )
        db_result = result_crud.add_result(
            db=db,
            storage=storage,
            session_id=session_id,
            result=result_schemas.ResultBaseSchema(
                name=f"{gt_trajectory.name} vs {est_trajectory.name}"
            ),
            report=report,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return db_result


@router.post("/trajectories/plot", response_model=result_schemas.ResultSchema)
async def plot_trajectories_endpoint(
    session_id: str,
    trajectories: list[Trajectory] = Depends(get_trajectories),
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    try:
        report = create_plot_report(
            trajectories=trajectories, settings=settings_schemas.SettingsSchema()
        )
        db_result = result_crud.add_result(
            db=db,
            storage=storage,
            session_id=session_id,
            result=result_schemas.ResultBaseSchema(name="Trajectory plot"),
            report=report,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return db_result
