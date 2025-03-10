import uuid

from app import dtos
from app.dependencies import get_db
from app.exceptions import (SessionNotFoundException,
                            TrajectoryNotFoundException)
from app.repository import models
from fastapi import Depends
from sqlalchemy.orm import Session
from trajectopy import Trajectory


class TrajectoryRepository:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def add_trajectory(
        self,
        trajectory: Trajectory,
        session_id: str,
    ) -> models.Trajectory:
        duration = trajectory.tstamps[-1] - trajectory.tstamps[0]
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)

        duration_str = f"{hours:02}h {minutes:02}m {seconds:02}s"

        db_trajectory = self.create_trajectory(
            dtos.CreateTrajectoryDTO(
                name=trajectory.name,
                epsg=trajectory.pos.epsg,
                num_poses=len(trajectory),
                session_id=session_id,
                has_orientations=trajectory.has_orientation,
                datarate=trajectory.data_rate,
                duration=duration_str,
            ),
        )

        return db_trajectory

    def create_trajectory(
        self,
        trajectory: dtos.CreateTrajectoryDTO,
        settings: dtos.SettingsDTO = dtos.SettingsDTO(),
    ) -> models.Trajectory:
        db_trajectory = models.Trajectory(
            **trajectory.model_dump(), id=uuid.uuid4().hex, settings=settings.model_dump()
        )
        self.db.add(db_trajectory)
        self.db.commit()
        self.db.refresh(db_trajectory)
        return db_trajectory

    def get_trajectories_of_session(self, session_id: str) -> list[models.Trajectory]:
        session = self.db.query(models.Session).filter(models.Session.id == session_id).first()

        if session is None:
            raise SessionNotFoundException(session_id)

        return session.trajectories

    def get_trajectory(self, trajectory_id: str) -> models.Trajectory:
        trajectory = self.db.query(models.Trajectory).filter(models.Trajectory.id == trajectory_id).first()

        if trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        return trajectory

    def get_settings(self, trajectory_id: str) -> dict:
        trajectory = self.db.query(models.Trajectory).filter(models.Trajectory.id == trajectory_id).first()

        if trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        return trajectory.settings

    def update_settings(self, trajectory_id: str, settings: dtos.SettingsDTO) -> None:
        trajectory = self.db.query(models.Trajectory).filter_by(id=trajectory_id)

        if trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        trajectory.update({"settings": settings.model_dump()})
        self.db.commit()

    def update_single_settings(self, trajectory_id: str, settings: dict) -> None:
        trajectory = self.db.query(models.Trajectory).filter_by(id=trajectory_id)

        if trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        trajectory.update({"settings": settings})
        self.db.commit()

    def delete_trajectory(self, trajectory_id: str) -> None:
        trajectory = self.db.query(models.Trajectory).filter_by(id=trajectory_id)

        if trajectory is None:
            raise TrajectoryNotFoundException(trajectory_id)

        trajectory.delete()
        self.db.commit()
