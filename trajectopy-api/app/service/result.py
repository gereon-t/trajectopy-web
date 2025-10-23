from app.dependencies import get_storage
from app.dtos import ResultDTO
from app.repository.result import ResultRepository
from app.storage import StorageProtocol
from fastapi import Depends, Response


class ResultService:

    def __init__(
        self,
        result_repository: ResultRepository = Depends(ResultRepository),
        storage: StorageProtocol = Depends(get_storage),
    ):
        self.result_repository = result_repository
        self.storage = storage

    def delete_result(self, result_id: str) -> None:
        result = self.result_repository.get_result(result_id)
        self.storage.remove_result(session_id=result.session_id, result_id=result.id)
        self.result_repository.delete_result(result.id)

    def get_result(self, result_id: str) -> ResultDTO:
        return ResultDTO.model_validate(self.result_repository.get_result(result_id))

    def render_result(self, result_id: str) -> Response:
        result = self.result_repository.get_result(result_id)
        report = self.storage.read_result(result.session_id, result.id)
        return Response(report, media_type="text/html")

    def get_results(self, session_id: str) -> list[ResultDTO]:
        return [ResultDTO.model_validate(r) for r in self.result_repository.get_results_of_session(session_id)]
