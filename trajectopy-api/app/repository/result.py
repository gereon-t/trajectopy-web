from app.dependencies import get_db
from app.exceptions import ResultNotFoundException
from app.repository import models
from fastapi import Depends
from sqlalchemy.orm import Session


class ResultRepository:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_result(self, result: models.Result) -> models.Result:
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    def get_result(self, result_id: str) -> models.Result:
        result = self.db.query(models.Result).filter(models.Result.id == result_id).first()

        if result is None:
            raise ResultNotFoundException(f"Result with id {result_id} not found")

        return result

    def delete_result(self, result_id: str) -> None:
        self.db.query(models.Result).filter_by(id=result_id).delete()
        self.db.commit()
