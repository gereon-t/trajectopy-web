from enum import Enum

import numpy as np
from pydantic import BaseModel


class MatchingMethod(str, Enum):
    NEAREST_SPATIAL = "nearest_spatial"
    NEAREST_TEMPORAL = "nearest_temporal"
    INTERPOLATION = "interpolation"
    NEAREST_SPATIAL_INTERPOLATION = "nearest_spatial_interpolation"


class Unit(str, Enum):
    METER = "meter"
    MILLIMETER = "millimeter"
    SECOND = "second"


class ExportFormat(str, Enum):
    PNG = "png"
    SVG = "svg"
    JPEG = "jpeg"
    WEBP = "webp"


class SettingsSchema(BaseModel):
    rpe_enabled: bool = True
    alignment_min_speed: float = 0.0
    alignment_time_start: float = 0.0
    alignment_time_end: float = 0.0
    alignment_trans_x: bool = True
    alignment_trans_y: bool = True
    alignment_trans_z: bool = True
    alignment_rot_x: bool = True
    alignment_rot_y: bool = True
    alignment_rot_z: bool = True
    alignment_scale: bool = False
    alignment_time_shift: bool = False
    alignment_use_x_speed: bool = True
    alignment_use_y_speed: bool = True
    alignment_use_z_speed: bool = True
    alignment_lever_x: bool = False
    alignment_lever_y: bool = False
    alignment_lever_z: bool = False
    alignment_sensor_rotation: bool = False
    alignment_auto_update: bool = False
    alignment_std_xyz_from: float = 1.0
    alignment_std_xyz_to: float = 1.0
    alignment_std_z_from: float = 1.0
    alignment_std_z_to: float = 1.0
    alignment_std_roll_pitch: float = np.deg2rad(1.0)
    alignment_std_yaw: float = np.deg2rad(1.0)
    alignment_std_speed: float = 1.0
    alignment_error_probability: float = 0.05

    matching_method: MatchingMethod = MatchingMethod.INTERPOLATION
    matching_max_time_diff: float = 0.01
    matching_max_dist_diff: float = 0.0
    matching_k_nearest: int = 10

    rpe_min_distance: float = 100.0
    rpe_max_distance: float = 800.0
    rpe_distance_step: float = 100.0
    rpe_distance_unit: Unit = Unit.METER
    rpe_use_all_pairs: bool = True

    report_scatter_max_std: float = 4.0
    report_ate_unit: Unit = Unit.MILLIMETER
    report_directed_ate: bool = True
    report_histogram_opacity: float = 0.6
    report_histogram_bargap: float = 0.1
    report_histogram_barmode: str = "overlay"
    report_histogram_yaxis_title: str = "Count"
    report_plot_mode: str = "lines+markers"
    report_scatter_mode: str = "markers"
    report_colorscale: str = "RdYlBu_r"
    report_x_name: str = "x"
    report_y_name: str = "y"
    report_z_name: str = "z"
    report_x_unit: str = "m"
    report_y_unit: str = "m"
    report_z_unit: str = "m"
    report_rot_x_name: str = "roll"
    report_rot_y_name: str = "pitch"
    report_rot_z_name: str = "yaw"
    report_rot_unit: str = "°"
    report_single_height: int = 450
    report_double_height: int = 540
    report_triple_height: int = 750

    export_single_format: ExportFormat = ExportFormat.PNG
    export_single_height: int = 500
    export_single_width: int = 800
    export_single_scale: float = 6.0

    export_double_format: ExportFormat = ExportFormat.PNG
    export_double_height: int = 500
    export_double_width: int = 800
    export_double_scale: float = 6.0

    export_triple_format: ExportFormat = ExportFormat.PNG
    export_triple_height: int = 500
    export_triple_width: int = 800
    export_triple_scale: float = 6.0

    class Config:
        from_attributes = True
