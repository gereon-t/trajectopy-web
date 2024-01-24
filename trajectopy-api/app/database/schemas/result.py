from pydantic import BaseModel


class ResultBaseSchema(BaseModel):
    name: str


class ResultSchema(ResultBaseSchema):
    id: str
    session_id: str

    class Config:
        from_attributes = True


class AlignmentResultSchema(BaseModel):
    aligned_trajectory_id: str
    trans_x: float
    trans_y: float
    trans_z: float
    rot_x: float
    rot_y: float
    rot_z: float
    scale: float
    lever_x: float
    lever_y: float
    lever_z: float

    sensor_rot_x: float
    sensor_rot_y: float
    sensor_rot_z: float
