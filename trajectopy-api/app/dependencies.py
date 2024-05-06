import os

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.orm import Session
from trajectopy_core.trajectory import Trajectory

from app.database import SessionLocal
from app.database.crud import trajectory as trajectory_crud
from app.storage.backends.azure import AzureStorage
from app.storage.backends.local import LocalStorage
from app.storage.storage_protocol import StorageProtocol

load_dotenv()

STORAGE_BACKENDS = {"local": LocalStorage, "azure": AzureStorage}


def get_storage():
    backend_config = os.getenv("STORAGE_BACKEND", "local")

    if backend_config == "azure":
        return AzureStorage()

    if backend_config == "local":
        return LocalStorage(os.getenv("DATA_PATH", "./data"))

    raise ValueError(f"Invalid storage backend: {backend_config}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_trajectory(
    session_id: str, trajectory_id: str, storage: StorageProtocol
) -> Trajectory:
    try:
        return storage.read_trajectory(
            session_id=session_id, trajectory_id=trajectory_id
        )
    except Exception as e:
        return None


def get_trajectory(
    session_id: str,
    trajectory_id: str,
    storage: StorageProtocol = Depends(get_storage),
) -> Trajectory:
    return load_trajectory(session_id, trajectory_id, storage)


def get_gt_trajectory(
    session_id: str,
    gt_trajectory_id: str,
    storage: StorageProtocol = Depends(get_storage),
) -> Trajectory:
    return load_trajectory(session_id, gt_trajectory_id, storage)


def get_est_trajectory(
    session_id: str,
    est_trajectory_id: str,
    storage: StorageProtocol = Depends(get_storage),
) -> Trajectory:
    return load_trajectory(session_id, est_trajectory_id, storage)


def get_trajectories(
    trajectory_ids: list[str],
    db: Session = Depends(get_db),
    storage: StorageProtocol = Depends(get_storage),
) -> list[Trajectory]:
    trajectories = []

    for traj_id in trajectory_ids:
        db_trajectory = trajectory_crud.get_trajectory(db, traj_id)

        if db_trajectory is None:
            continue

        trajectories.append(
            load_trajectory(db_trajectory.session_id, db_trajectory.id, storage)
        )

    return trajectories
