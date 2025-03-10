import os
import shutil
from typing import Protocol

from app.exceptions import (ResultNotFoundException, SessionNotFoundException,
                            TrajectoryNotFoundException)
from trajectopy import Trajectory


class StorageProtocol(Protocol):
    def create_session(self, session_id: str) -> None:
        """
        Adds a new session to the storage

        Args:
            session_id (str): Id of the created session.
        """

    def delete_session(self, session_id: str) -> None:
        """
        Deletes a session from the storage

        Args:
            session_id (str): Unique id of the session
        """

    def write_trajectory(self, session_id: str, trajectory_id: str, trajectory: Trajectory) -> None:
        """
        Adds a trajectory to a session

        Args:
            session_id (str): Unique id of the session
            trajectory (Trajectory): Trajectory object to write to the storage
            trajectory_id (str): Id of the written trajectory.
        """

    def write_result(self, session_id: str, result_id: str, result: str) -> None:
        """
        Writes a result to JSON

        Args:
            session_id (str): Unique id of the session
            result (str): Result str (html) to write to the storage
            result_id (str): Id of the result.
        """

    def remove_trajectory(self, session_id: str, trajectory_id: str) -> None:
        """
        Removes a trajectory from a session

        Args:
            session_id (str): Unique id of the session
            trajectory_id (str): Trajectory id
        """

    def remove_result(self, session_id: str, result_id: str) -> None:
        """
        Removes a result

        Args:
            session_id (str): Unique id of the session
            result_id (str): result_id
        """

    def read_trajectory(self, session_id: str, trajectory_id: str) -> Trajectory:
        """
        Reads a trajectory from a session

        Args:
            session_id (str): Unique id of the session
            trajectory_id (str): Trajectory id

        Returns:
            Trajectory: Trajectory object
        """

    def read_result(self, session_id: str, result_id: str) -> str:
        """
        Reads a result from a session

        Args:
            session_id (str): Unique id of the session
            result_id (str): Result id
        """


class LocalStorage:
    def __init__(self, data_path: str) -> None:
        self.data_path = os.path.abspath(data_path)

        if os.path.exists(data_path):
            return

        os.mkdir(self.data_path)

    def create_session(self, session_id: str) -> None:
        """
        Adds a new session to the storage

        Args:
            session_id (str): Id of the created session.
        """
        if os.path.exists(os.path.join(self.data_path, session_id)):
            return

        os.mkdir(os.path.join(self.data_path, session_id))

    def delete_session(self, session_id: str) -> None:
        """
        Deletes a session from the storage

        Args:
            session_id (str): Unique id of the session
        """
        if not os.path.exists(os.path.join(self.data_path, session_id)):
            return

        shutil.rmtree(os.path.join(self.data_path, session_id))

    def write_trajectory(self, session_id: str, trajectory_id: str, trajectory: Trajectory) -> None:
        """
        Adds a trajectory to a session

        Args:
            session_id (str): Unique id of the session
            trajectory (Trajectory): Trajectory object to write to the storage
            trajectory_id (str): Id of the written trajectory.
        """
        if not os.path.exists(os.path.join(self.data_path, session_id)):
            self.create_session(session_id)

        trajectory.to_file(f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj")

    def read_trajectory(self, session_id: str, trajectory_id: str) -> Trajectory:
        """
        Reads a trajectory from a session

        Args:
            session_id (str): Unique id of the session
            trajectory_id (str): Trajectory id
        """
        if not os.path.exists(os.path.join(self.data_path, session_id)):
            raise SessionNotFoundException(session_id)

        if not os.path.exists(f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj"):
            raise TrajectoryNotFoundException(trajectory_id)

        return Trajectory.from_file(f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj")

    def write_result(self, session_id: str, result_id: str, result: str) -> None:
        """
        Writes a result to HTML

        Args:
            session_id (str): Unique id of the session
            result (str): Result str (html) to write to the storage
            result_id (str): Id of the result.
        """
        if not os.path.exists(os.path.join(self.data_path, session_id)):
            self.create_session(session_id)

        with open(
            f"{os.path.join(self.data_path, session_id, result_id)}.html",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(result)

    def read_result(self, session_id: str, result_id: str) -> str:
        """
        Reads a result from a session

        Args:
            session_id (str): Unique id of the session
            result_id (str): Result id
        """
        if not os.path.exists(os.path.join(self.data_path, session_id)):
            raise SessionNotFoundException(session_id)

        if not os.path.exists(f"{os.path.join(self.data_path, session_id, result_id)}.html"):
            raise ResultNotFoundException(result_id)

        with open(
            f"{os.path.join(self.data_path, session_id, result_id)}.html",
            "r",
            encoding="utf-8",
        ) as f:
            return f.read()

    def remove_trajectory(self, session_id: str, trajectory_id: str) -> None:
        """
        Removes a trajectory from a session

        Args:
            session_id (str): Unique id of the session
            trajectory_id (str): Trajectory id
        """
        if not os.path.exists(f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj"):
            return

        os.remove(f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj")

    def remove_result(self, session_id: str, result_id: str) -> None:
        """
        Removes a result from a session

        Args:
            session_id (str): Unique id of the session
            result_id (str): Result id
        """
        if not os.path.exists(f"{os.path.join(self.data_path, session_id, result_id)}.html"):
            return

        os.remove(f"{os.path.join(self.data_path, session_id, result_id)}.html")
