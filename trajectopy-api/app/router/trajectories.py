from app import dtos
from app.service.trajectory import TrajectoryService
from fastapi import APIRouter, Depends, Response, UploadFile
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/trajectories", tags=["Trajectories"])


@router.get("/")
async def get_trajectories_endpoint(
    session_id: str, trajectory_service: TrajectoryService = Depends(TrajectoryService)
) -> list[dtos.TrajectoryDTO]:
    return trajectory_service.get_trajectories_of_session(session_id)


@router.get("/{trajectory_id}")
async def get_trajectory_endpoint(
    trajectory_id: str,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> dtos.TrajectoryDTO:
    return trajectory_service.get_trajectory(trajectory_id)


@router.post("/upload", status_code=201)
async def upload_trajectory_endpoint(
    session_id: str,
    file: UploadFile,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> dtos.TrajectoryDTO:
    return trajectory_service.upload_trajectory(session_id, file)


@router.delete("/{trajectory_id}", status_code=204)
async def delete_trajectory_endpoint(
    trajectory_id: str,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> Response:
    trajectory_service.delete_trajectory(trajectory_id)


@router.get("/download/{trajectory_id}")
async def download_trajectory_endpoint(
    session_id: str,
    trajectory_id: str,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> PlainTextResponse:
    return trajectory_service.download_trajectory(session_id=session_id, trajectory_id=trajectory_id)


@router.get("/positions/{session_id}/{trajectory_id}")
async def get_trajectory_positions_endpoint(
    session_id: str,
    trajectory_id: str,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
    epsg: int = 4326,
) -> dtos.TrajectoryPositionsDTO:
    return trajectory_service.get_trajectory_positions(session_id=session_id, trajectory_id=trajectory_id, epsg=epsg)


@router.post("/compare", status_code=201)
async def compare_trajectories_endpoint(
    session_id: str,
    gt_trajectory_id: str,
    est_trajectory_id: str,
    settings: dtos.SettingsDTO = dtos.SettingsDTO(),
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> dtos.ResultDTO:
    return trajectory_service.compare_trajectories(
        session_id=session_id,
        gt_trajectory_id=gt_trajectory_id,
        est_trajectory_id=est_trajectory_id,
        settings=settings,
    )


@router.post("/plot", status_code=201)
async def plot_trajectories_endpoint(
    session_id: str,
    trajectory_ids: list[str],
    plot_on_map: bool = False,
    map_style: str = "open-street-map",
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> dtos.ResultDTO:
    return trajectory_service.plot_trajectories(session_id, trajectory_ids, plot_on_map, map_style)
