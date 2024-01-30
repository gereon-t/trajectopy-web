from enum import Enum
from pydantic import BaseModel


class Unit(str, Enum):
    METER = "meter"
    SECOND = "second"


class SettingsSchema(BaseModel):
    ate_in_mm: bool = False
    directed_ate: bool = False
    similarity_transformation: bool = True
    lever_arm_estimation: bool = False
    time_shift_estimation: bool = False
    sensor_rotation_estimation: bool = False
    rpe_enabled: bool = True
    rpe_min_distance: float = 100.0
    rpe_max_distance: float = 800.0
    rpe_distance_step: float = 100.0
    rpe_distance_unit: str = "meter"
    rpe_use_all_pairs: bool = True

    class Config:
        from_attributes = True
