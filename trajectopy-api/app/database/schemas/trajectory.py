from pydantic import BaseModel

from app.database.schemas.settings import SettingsSchema


class TrajectoryBaseSchema(BaseModel):
    name: str
    epsg: int
    session_id: str


class TrajectoryCreateSchema(TrajectoryBaseSchema):
    settings: SettingsSchema


class TrajectorySchema(TrajectoryBaseSchema):
    id: str

    class Config:
        from_attributes = True
