from pydantic import BaseModel


class ResultDTO(BaseModel):
    id: str
    name: str
    session_id: str

    class Config:
        from_attributes = True


class SettingsDTO(BaseModel):
    ate_in_mm: bool = False
    directed_ate: bool = False
    matching: str = "interpolation"
    similarity_transformation: bool = True
    scale_estimation: bool = False
    lever_arm_estimation: bool = False
    time_shift_estimation: bool = False
    sensor_rotation_estimation: bool = False
    rpe_enabled: bool = True
    rpe_min_distance: float = 100.0
    rpe_max_distance: float = 800.0
    rpe_distance_step: float = 100.0
    rpe_distance_unit: str = "meter"
    rpe_use_all_pairs: bool = True
    plot_on_map: bool = False
    map_style: str = "open-street-map"

    class Config:
        from_attributes = True


class CreateTrajectoryDTO(BaseModel):
    name: str
    duration: str
    datarate: float
    epsg: int
    num_poses: int
    has_orientations: bool = False
    session_id: str


class TrajectoryDTO(CreateTrajectoryDTO):
    id: str
    settings: SettingsDTO

    class Config:
        from_attributes = True


class SessionDTO(BaseModel):
    id: str
    date: str
    trajectories: list[TrajectoryDTO] = []

    class Config:
        from_attributes = True
