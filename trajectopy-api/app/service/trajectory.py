import uuid

from app import dtos
from app.dependencies import get_storage
from app.exceptions import SessionNotFoundException, TrajectoryNotFoundException
from app.repository import models
from app.repository.result import ResultRepository
from app.repository.session import SessionRepository
from app.repository.trajectory import TrajectoryRepository
from app.storage import StorageProtocol
from app.utils import create_comparison_report, create_plot_report
from fastapi import Depends, UploadFile
from fastapi.responses import PlainTextResponse
from trajectopy import Trajectory


class TrajectoryService:

    def __init__(
        self,
        trajectory_repository: TrajectoryRepository = Depends(TrajectoryRepository),
        session_repository: SessionRepository = Depends(SessionRepository),
        result_respository: ResultRepository = Depends(ResultRepository),
        storage: StorageProtocol = Depends(get_storage),
    ):
        self.trajectory_repository = trajectory_repository
        self.session_repository = session_repository
        self.result_respository = result_respository
        self.storage = storage

    def get_trajectories_of_session(self, session_id: str) -> list[dtos.TrajectoryDTO]:
        return [
            dtos.TrajectoryDTO.model_validate(t)
            for t in self.trajectory_repository.get_trajectories_of_session(session_id)
        ]

    def get_trajectory(self, trajectory_id: str) -> dtos.TrajectoryDTO:
        return dtos.TrajectoryDTO.model_validate(self.trajectory_repository.get_trajectory(trajectory_id))

    def upload_trajectory(
        self,
        session_id: str,
        file: UploadFile,
    ) -> dtos.TrajectoryDTO:
        if self.session_repository.get_session(session_id) is None:
            raise SessionNotFoundException(session_id)

        input_stream = str(file.file.read(), encoding="utf-8")

        read_trajectory = Trajectory.from_file(input_stream, io_stream=True)
        db_trajectory = self.trajectory_repository.add_trajectory(read_trajectory, session_id)
        self.storage.write_trajectory(
            session_id=session_id,
            trajectory_id=db_trajectory.id,
            trajectory=read_trajectory,
        )

        return dtos.TrajectoryDTO.model_validate(db_trajectory)

    def delete_trajectory(self, trajectory_id: str) -> None:
        trajectory = self.trajectory_repository.get_trajectory(trajectory_id)

        self.trajectory_repository.delete_trajectory(trajectory_id)
        self.storage.remove_trajectory(session_id=trajectory.session_id, trajectory_id=trajectory_id)

    def download_trajectory(
        self,
        session_id: str,
        trajectory_id: str,
    ) -> PlainTextResponse:
        trajectory = self.storage.read_trajectory(session_id=session_id, trajectory_id=trajectory_id)
        csv_data = str(trajectory.to_dataframe().to_csv(index=False))

        return PlainTextResponse(csv_data, media_type="text/csv")

    def compare_trajectories(
        self,
        session_id: str,
        gt_trajectory_id: str,
        est_trajectory_id: str,
        settings: dtos.SettingsDTO = dtos.SettingsDTO(),
    ) -> dtos.ResultDTO:
        gt_trajectory = self.storage.read_trajectory(session_id, gt_trajectory_id)
        est_trajectory = self.storage.read_trajectory(session_id, est_trajectory_id)

        report = create_comparison_report(gt_traj=gt_trajectory, est_traj=est_trajectory, settings=settings)

        db_result = self.result_respository.create_result(
            models.Result(
                name=f"{gt_trajectory.name} vs {est_trajectory.name}",
                id=uuid.uuid4().hex,
                session_id=session_id,
            )
        )
        self.storage.write_result(session_id=session_id, result_id=db_result.id, result=report)

        return dtos.ResultDTO.model_validate(db_result)

    def plot_trajectories(
        self,
        session_id: str,
        trajectory_ids: list[str],
        plot_on_map: bool = False,
        map_style: str = "open-street-map",
    ) -> dtos.ResultDTO:
        trajectories = [self.storage.read_trajectory(session_id, traj_id) for traj_id in trajectory_ids]

        report = create_plot_report(
            trajectories=trajectories, settings=dtos.SettingsDTO(plot_on_map=plot_on_map, map_style=map_style)
        )
        db_result = self.result_respository.create_result(
            models.Result(
                name="Trajectory plot",
                id=uuid.uuid4().hex,
                session_id=session_id,
            )
        )
        self.storage.write_result(session_id=session_id, result_id=db_result.id, result=report)

        return dtos.ResultDTO.model_validate(db_result)

    def update_settings(
        self,
        trajectory_id: str,
        settings: dtos.SettingsDTO,
    ) -> None:
        db_trajectory = self.trajectory_repository.get_trajectory(trajectory_id)

        if db_trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        self.trajectory_repository.update_settings(trajectory_id, settings)

    def update_single_settings(self, trajectory_id: str, settings: dict) -> None:
        db_trajectory = self.trajectory_repository.get_trajectory(trajectory_id)

        if db_trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        self.trajectory_repository.update_single_settings(trajectory_id, settings)

    def get_settings(self, trajectory_id: str) -> dtos.SettingsDTO:
        db_trajectory = self.trajectory_repository.get_trajectory(trajectory_id)

        if db_trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        return dtos.SettingsDTO(**self.trajectory_repository.get_settings(trajectory_id))
