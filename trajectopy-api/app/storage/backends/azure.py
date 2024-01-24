import logging
import os

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from trajectopy_core.trajectory import Trajectory

load_dotenv()

ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
ENDPOINT_SUFFIX = os.getenv("ENDPOINT_SUFFIX")
PROTOCOL = os.getenv("PROTOCOL")
ACCOUNT_URL = f"{PROTOCOL}://{ACCOUNT_NAME}.{ENDPOINT_SUFFIX}"

CONNECTION_STR = os.getenv("CONNECTION_STR")

IGNORED_CONTAINERS = [
    "azure-pipelines-deploy",
    "azure-webjobs-hosts",
    "azure-webjobs-secrets",
    "scm-releases",
]


class StorageException(Exception):
    pass


def storage_exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error("Exception: %s", e)
            raise StorageException(e) from e

    return wrapper


class AzureStorage:
    def __init__(self):
        pass

    @storage_exception_handler
    def get_service_client(self) -> BlobServiceClient:
        return BlobServiceClient(account_url=ACCOUNT_URL, credential=CONNECTION_STR)

    @storage_exception_handler
    def list_containers(self):
        return self.get_service_client().list_containers()

    @storage_exception_handler
    def list_blobs(self, container_name: str):
        container_client = self.get_service_client().get_container_client(
            container_name
        )
        return container_client.list_blobs()

    @storage_exception_handler
    def upload_blob(self, container_name: str, blob_name: str, data: bytes) -> str:
        container_client = self.get_service_client().get_container_client(
            container_name
        )

        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        return blob_name

    @storage_exception_handler
    def download_blob(self, container_name: str, blob_name: str) -> bytes:
        container_client = self.get_service_client().get_container_client(
            container_name
        )
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    @storage_exception_handler
    def delete_blob(self, container_name: str, blob_name: str) -> None:
        container_client = self.get_service_client().get_container_client(
            container_name
        )
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.delete_blob()

    @storage_exception_handler
    def create_container(self, container_name: str) -> str:
        container_client = self.get_service_client().get_container_client(
            container_name
        )
        container_client.create_container()
        return container_name

    @storage_exception_handler
    def delete_container(self, container_name: str) -> None:
        container_client = self.get_service_client().get_container_client(
            container_name
        )
        container_client.delete_container()

    @storage_exception_handler
    def contains(self, container_name: str) -> bool:
        return container_name in self.list_container_names()

    def contains_blob(self, container_name: str, blob_name: str) -> bool:
        if not self.contains(container_name):
            return False

        container_client = self.get_service_client().get_container_client(
            container_name
        )

        return blob_name in container_client.list_blob_names()

    @storage_exception_handler
    def list_container_names(self) -> list[str]:
        return [
            container.name for container in self.get_service_client().list_containers()
        ]

    @storage_exception_handler
    def list_blob_names(self, container_name: str) -> list[str]:
        container_client = self.get_service_client().get_container_client(
            container_name
        )
        return list(container_client.list_blob_names())

    def create_session(self, session_id: str) -> None:
        """
        Adds a new session to the storage

        Args:
            session_id (str): Id of the created session.
        """
        self.create_container(session_id)

    def delete_session(self, session_id: str) -> None:
        """
        Deletes a session from the storage

        Args:
            session_id (str): Unique id of the session
        """
        self.delete_container(session_id)

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
        fields = (
            "t,l,px,py,pz,vx,vy,vz"
            if trajectory.rot is None
            else "t,l,px,py,pz,qx,qy,qz,qw,vx,vy,vz"
        )
        csv_data = trajectory.to_dataframe().to_csv(index=False).split("\n", 1)[1]
        filestr = f"#epsg {trajectory.pos.epsg}\n#name {trajectory.name}\n#nframe enu\n#fields {fields}\n{csv_data}"
        self.upload_blob(
            container_name=session_id,
            blob_name=f"{trajectory_id}.traj",
            data=filestr.encode("utf-8"),
        )

    def write_result(self, session_id: str, result_id: str, result: str) -> None:
        """
        Writes a result to JSON

        Args:
            session_id (str): Unique id of the session
            result (str): Result str (html) to write to the storage
            result_id (str): Id of the result.
        """
        self.upload_blob(
            container_name=session_id,
            blob_name=f"{result_id}.html",
            data=result.encode("utf-8"),
        )

    def remove_trajectory(self, session_id: str, trajectory_id: str) -> None:
        """
        Removes a trajectory from a session

        Args:
            session_id (str): Unique id of the session
            trajectory_id (str): Trajectory id
        """
        self.delete_blob(container_name=session_id, blob_name=f"{trajectory_id}.traj")

    def remove_result(self, session_id: str, result_id: str) -> None:
        """
        Removes a result

        Args:
            session_id (str): Unique id of the session
            result_id (str): result_id
        """
        self.delete_blob(container_name=session_id, blob_name=f"{result_id}.html")

    def read_trajectory(self, session_id: str, trajectory_id: str) -> Trajectory:
        """
        Reads a trajectory from a session

        Args:
            session_id (str): Unique id of the session
            trajectory_id (str): Trajectory id

        Returns:
            Trajectory: Trajectory object
        """
        csv_data = self.download_blob(
            container_name=session_id, blob_name=f"{trajectory_id}.traj"
        )
        return Trajectory.from_file(csv_data.decode("utf-8"), io_stream=True)

    def read_result(self, session_id: str, result_id: str) -> str:
        """
        Reads a result from a session

        Args:
            session_id (str): Unique id of the session
            result_id (str): Result id
        """
        return self.download_blob(
            container_name=session_id, blob_name=f"{result_id}.html"
        ).decode("utf-8")
