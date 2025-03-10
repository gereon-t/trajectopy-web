from app.dtos import SettingsDTO
from app.service.trajectory import TrajectoryService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.put("/update", status_code=204)
async def update_settings_endpoint(
    trajectory_id: str,
    settings: SettingsDTO,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> None:
    trajectory_service.update_settings(trajectory_id, settings)


@router.put("/update/single", status_code=204)
async def update_single_settings_endpoint(
    trajectory_id: str,
    settings: dict,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> None:
    trajectory_service.update_single_settings(trajectory_id, settings)


@router.get("/{trajectory_id}")
async def get_settings_endpoint(
    trajectory_id: str,
    trajectory_service: TrajectoryService = Depends(TrajectoryService),
) -> SettingsDTO:
    return trajectory_service.get_settings(trajectory_id)
