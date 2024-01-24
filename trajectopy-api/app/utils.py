from trajectopy_core.alignment.result import AlignmentResult
from trajectopy_core.definitions import Unit
from trajectopy_core.pipelines import ate, rpe
from trajectopy_core.report.single import render_single_report
from trajectopy_core.report.trajectory import render_trajectories
from trajectopy_core.settings.alignment import (
    AlignmentEstimationSettings,
    AlignmentPreprocessing,
    AlignmentSettings,
    AlignmentStochastics,
)
from trajectopy_core.settings.comparison import RelativeComparisonSettings
from trajectopy_core.settings.matching import MatchingMethod, MatchingSettings
from trajectopy_core.settings.processing import ProcessingSettings
from trajectopy_core.settings.report import ExportSettings, ReportSettings
from trajectopy_core.trajectory import Trajectory

from app.database.schemas.result import AlignmentResultSchema
from app.database.schemas.settings import SettingsSchema

UNIT_DICT = {"meter": Unit.METER, "second": Unit.SECOND}


def create_plot_report(trajectories: list[Trajectory], settings: SettingsSchema):
    report_settings = to_report_settings(settings)

    return render_trajectories(
        trajectories=trajectories, report_settings=report_settings
    )


def create_comparison_report(
    gt_traj: Trajectory, est_traj: Trajectory, settings: SettingsSchema
):
    processing_settings = to_processing_settings(settings)
    report_settings = to_report_settings(settings)

    if (
        gt_traj.pos.local_transformer is not None
        and est_traj.pos.local_transformer is not None
    ):
        est_traj.pos.local_transformer = gt_traj.pos.local_transformer
        est_traj.pos.to_epsg(gt_traj.pos.epsg)

    ate_result = ate(
        trajectory_gt=gt_traj, trajectory_est=est_traj, settings=processing_settings
    )
    rpe_result = (
        rpe(
            trajectory_gt=gt_traj, trajectory_est=est_traj, settings=processing_settings
        )
        if settings.rpe_enabled
        else None
    )

    return render_single_report(
        ate_result=ate_result, rpe_result=rpe_result, report_settings=report_settings
    )


def to_alignment_estimation_settings(
    settings: SettingsSchema,
) -> AlignmentEstimationSettings:
    return AlignmentEstimationSettings(
        trans_x=settings.alignment_trans_x,
        trans_y=settings.alignment_trans_y,
        trans_z=settings.alignment_trans_z,
        rot_x=settings.alignment_rot_x,
        rot_y=settings.alignment_rot_y,
        rot_z=settings.alignment_rot_z,
        scale=settings.alignment_scale,
        time_shift=settings.alignment_time_shift,
        use_x_speed=settings.alignment_use_x_speed,
        use_y_speed=settings.alignment_use_y_speed,
        use_z_speed=settings.alignment_use_z_speed,
        lever_x=settings.alignment_lever_x,
        lever_y=settings.alignment_lever_y,
        lever_z=settings.alignment_lever_z,
        sensor_rotation=settings.alignment_sensor_rotation,
        auto_update=settings.alignment_auto_update,
    )


def to_alignment_stochastics(
    settings: SettingsSchema,
) -> AlignmentStochastics:
    return AlignmentStochastics(
        std_xy_from=settings.alignment_std_xyz_from,
        std_xy_to=settings.alignment_std_xyz_to,
        std_z_from=settings.alignment_std_z_from,
        std_z_to=settings.alignment_std_z_to,
        std_roll_pitch=settings.alignment_std_roll_pitch,
        std_yaw=settings.alignment_std_yaw,
        std_speed=settings.alignment_std_speed,
        error_probability=settings.alignment_error_probability,
    )


def to_alignment_preprocessing(
    settings: SettingsSchema,
) -> AlignmentPreprocessing:
    return AlignmentPreprocessing(
        min_speed=settings.alignment_min_speed,
        time_start=settings.alignment_time_start,
        time_end=settings.alignment_time_end,
    )


def to_alignment_settings(settings: SettingsSchema) -> AlignmentSettings:
    return AlignmentSettings(
        preprocessing=to_alignment_preprocessing(settings),
        estimation_of=to_alignment_estimation_settings(settings),
        stochastics=to_alignment_stochastics(settings),
    )


def to_matching_settings(settings: SettingsSchema) -> MatchingSettings:
    method_dict = {
        "nearest_spatial": MatchingMethod.NEAREST_SPATIAL,
        "nearest_temporal": MatchingMethod.NEAREST_TEMPORAL,
        "interpolation": MatchingMethod.INTERPOLATION,
        "nearest_spatial_interpolation": MatchingMethod.NEAREST_SPATIAL_INTERPOLATED,
    }
    return MatchingSettings(
        method=method_dict[settings.matching_method],
        max_time_diff=settings.matching_max_time_diff,
        max_distance=settings.matching_max_dist_diff,
        k_nearest=settings.matching_k_nearest,
    )


def to_relative_comparison_settings(
    settings: SettingsSchema,
) -> RelativeComparisonSettings:
    return RelativeComparisonSettings(
        pair_min_distance=settings.rpe_min_distance,
        pair_max_distance=settings.rpe_max_distance,
        pair_distance_step=settings.rpe_distance_step,
        pair_distance_unit=UNIT_DICT[settings.rpe_distance_unit],
        use_all_pose_pairs=settings.rpe_use_all_pairs,
    )


def to_report_settings(settings: SettingsSchema) -> ReportSettings:
    single_plot_export = ExportSettings(
        format=settings.export_single_format,
        height=settings.export_single_height,
        width=settings.export_single_width,
        scale=settings.export_single_scale,
    )

    double_plot_export = ExportSettings(
        format=settings.export_double_format,
        height=settings.export_double_height,
        width=settings.export_double_width,
        scale=settings.export_double_scale,
    )

    triple_plot_export = ExportSettings(
        format=settings.export_triple_format,
        height=settings.export_triple_height,
        width=settings.export_triple_width,
        scale=settings.export_triple_scale,
    )

    return ReportSettings(
        scatter_max_std=settings.report_scatter_max_std,
        ate_unit_is_mm=settings.report_ate_unit == "millimeter",
        directed_ate=settings.report_directed_ate,
        histogram_opacity=settings.report_histogram_opacity,
        histogram_bargap=settings.report_histogram_bargap,
        histogram_barmode=settings.report_histogram_barmode,
        histogram_yaxis_title=settings.report_histogram_yaxis_title,
        plot_mode=settings.report_plot_mode,
        scatter_mode=settings.report_scatter_mode,
        scatter_colorscale=settings.report_colorscale,
        pos_x_name=settings.report_x_name,
        pos_y_name=settings.report_y_name,
        pos_z_name=settings.report_z_name,
        pos_x_unit=settings.report_x_unit,
        pos_y_unit=settings.report_y_unit,
        pos_z_unit=settings.report_z_unit,
        rot_x_name=settings.report_rot_x_name,
        rot_y_name=settings.report_y_name,
        rot_z_name=settings.report_z_name,
        rot_unit=settings.report_x_unit,
        single_plot_height=settings.report_single_height,
        two_subplots_height=settings.report_double_height,
        three_subplots_height=settings.report_triple_height,
        single_plot_export=single_plot_export,
        two_subplots_export=double_plot_export,
        three_subplots_export=triple_plot_export,
    )


def to_processing_settings(settings: SettingsSchema) -> ProcessingSettings:
    alignment_settings = to_alignment_settings(settings)
    matching_settings = to_matching_settings(settings)
    relative_comparison_settings = to_relative_comparison_settings(settings)

    return ProcessingSettings(
        alignment=alignment_settings,
        matching=matching_settings,
        relative_comparison=relative_comparison_settings,
    )


def to_alignment_result_schema(
    alignment_result: AlignmentResult, trajectory_id: str
) -> AlignmentResultSchema:
    return AlignmentResultSchema(
        aligned_trajectory_id=trajectory_id,
        trans_x=alignment_result.position_parameters.sim_trans_x.value,
        trans_y=alignment_result.position_parameters.sim_trans_y.value,
        trans_z=alignment_result.position_parameters.sim_trans_z.value,
        rot_x=alignment_result.position_parameters.sim_rot_x.value,
        rot_y=alignment_result.position_parameters.sim_rot_y.value,
        rot_z=alignment_result.position_parameters.sim_rot_z.value,
        scale=alignment_result.position_parameters.sim_scale.value,
        lever_x=alignment_result.position_parameters.lever_x.value,
        lever_y=alignment_result.position_parameters.lever_y.value,
        lever_z=alignment_result.position_parameters.lever_z.value,
        sensor_rot_x=alignment_result.rotation_parameters.sensor_rot_x.value,
        sensor_rot_y=alignment_result.rotation_parameters.sensor_rot_y.value,
        sensor_rot_z=alignment_result.rotation_parameters.sensor_rot_z.value,
    )
