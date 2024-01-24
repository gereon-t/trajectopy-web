import os
import shutil

from trajectopy_core.trajectory import Trajectory


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
        os.mkdir(os.path.join(self.data_path, session_id))

    def delete_session(self, session_id: str) -> None:
        """
        Deletes a session from the storage

        Args:
            session_id (str): Unique id of the session
        """
        shutil.rmtree(os.path.join(self.data_path, session_id))

    def write_trajectory(
        self, session_id: str, trajectory_id: str, trajectory: Trajectory
    ) -> None:
        """
        Adds a trajectory to a session

        Args:
            session_id (str): Unique id of the session
            trajectory (Trajectory): Trajectory object to write to the storage
            trajectory_id (str): Id of the written trajectory.
        """
        trajectory.to_file(
            f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj"
        )

    def read_trajectory(self, session_id: str, trajectory_id: str) -> Trajectory:
        """
        Reads a trajectory from a session

        Args:
            session_id (str): Unique id of the session
            trajectory_id (str): Trajectory id
        """
        return Trajectory.from_file(
            f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj"
        )

    def write_result(self, session_id: str, result_id: str, result: str) -> None:
        """
        Writes a result to HTML

        Args:
            session_id (str): Unique id of the session
            result (str): Result str (html) to write to the storage
            result_id (str): Id of the result.
        """
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
        os.remove(f"{os.path.join(self.data_path, session_id, trajectory_id)}.traj")

    def remove_result(self, session_id: str, result_id: str) -> None:
        """
        Removes a result from a session

        Args:
            session_id (str): Unique id of the session
            result_id (str): Result id
        """
        os.remove(f"{os.path.join(self.data_path, session_id, result_id)}.html")
