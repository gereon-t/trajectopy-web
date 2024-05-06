import uuid

from sqlalchemy.orm import Session
from trajectopy_core.trajectory import Trajectory

from app.database import models
from app.database.schemas import settings as settings_schemas
from app.database.schemas import trajectory as trajectory_schemas
from app.storage.storage_protocol import StorageProtocol


def add_trajectory(
    db: Session,
    storage: StorageProtocol,
    trajectory: Trajectory,
    session_id: str,
) -> models.Trajectory:
    db_trajectory = create_trajectory(
        db,
        trajectory_schemas.TrajectoryBaseSchema(
            name=trajectory.name, epsg=trajectory.pos.epsg, session_id=session_id
        ),
        settings_schemas.SettingsSchema(),
    )

    storage.write_trajectory(
        session_id=session_id, trajectory_id=db_trajectory.id, trajectory=trajectory
    )

    return db_trajectory


def create_trajectory(
    db: Session,
    trajectory: trajectory_schemas.TrajectoryBaseSchema,
    settings: settings_schemas.SettingsSchema,
):
    db_trajectory = models.Trajectory(
        **trajectory.model_dump(), id=uuid.uuid4().hex, settings=settings.model_dump()
    )
    db.add(db_trajectory)
    db.commit()
    db.refresh(db_trajectory)
    return db_trajectory


def get_trajectories(db: Session, session_id: str):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    return session.trajectories if session else None


def get_trajectory(db: Session, trajectory_id: str):
    return (
        db.query(models.Trajectory)
        .filter(models.Trajectory.id == trajectory_id)
        .first()
    )


def get_settings(db: Session, trajectory_id: str):
    return (
        db.query(models.Trajectory)
        .filter(models.Trajectory.id == trajectory_id)
        .first()
        .settings
    )


def update_settings(
    db: Session, trajectory_id: str, settings: settings_schemas.SettingsSchema
):
    db.query(models.Trajectory).filter_by(id=trajectory_id).update(
        {"settings": settings.model_dump()}
    )
    db.commit()


def update_single_settings(db: Session, trajectory_id: str, settings: dict):
    db.query(models.Trajectory).filter_by(id=trajectory_id).update(
        {"settings": settings}
    )
    db.commit()


def delete_trajectory(db: Session, trajectory_id: str):
    db.query(models.Trajectory).filter_by(id=trajectory_id).delete()
    db.commit()
