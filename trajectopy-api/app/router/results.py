from app.dtos import ResultDTO
from app.service.result import ResultService
from fastapi import APIRouter, Depends, Response

router = APIRouter(prefix="/results", tags=["Results"])


@router.delete("/{result_id}", status_code=204)
async def delete_result_endpoint(result_id: str, result_service: ResultService = Depends(ResultService)) -> Response:
    result_service.delete_result(result_id)


@router.get("/{result_id}")
async def get_result_endpoint(result_id: str, result_service: ResultService = Depends(ResultService)) -> ResultDTO:
    return result_service.get_result(result_id)


@router.get("/render/{result_id}")
async def render_result_endpoint(
    result_id: str,
    result_service: ResultService = Depends(ResultService),
) -> Response:
    return result_service.render_result(result_id)
