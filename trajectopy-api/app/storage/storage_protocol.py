from typing import Protocol

from trajectopy_core.trajectory import Trajectory


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
