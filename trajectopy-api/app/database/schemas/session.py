from pydantic import BaseModel

from app.database.schemas.trajectory import TrajectorySchema


class SessionBaseSchema(BaseModel):
    id: str
    date: str


class SessionSchema(SessionBaseSchema):
    trajectories: list[TrajectorySchema] = []

    class Config:
        from_attributes = True
