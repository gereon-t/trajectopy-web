from trajectopy_core.alignment.result import AlignmentResult
from trajectopy_core.definitions import Unit
from trajectopy_core.pipelines import ate, rpe
from trajectopy_core.report.single import render_single_report
from trajectopy_core.report.trajectory import render_trajectories
from trajectopy_core.settings.alignment import (
    AlignmentEstimationSettings,
    AlignmentSettings,
)
from trajectopy_core.settings.comparison import RelativeComparisonSettings
from trajectopy_core.settings.processing import ProcessingSettings
from trajectopy_core.settings.report import ReportSettings
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
    return AlignmentEstimationSettings.from_components(
        similarity=settings.similarity_transformation,
        leverarm=settings.lever_arm_estimation,
        time_shift=settings.time_shift_estimation,
        sensor_rotation=settings.sensor_rotation_estimation,
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


def to_processing_settings(settings: SettingsSchema) -> ProcessingSettings:
    alignment_settings = AlignmentSettings(
        estimation_of=to_alignment_estimation_settings(settings)
    )
    relative_comparison_settings = to_relative_comparison_settings(settings)

    return ProcessingSettings(
        alignment=alignment_settings,
        relative_comparison=relative_comparison_settings,
    )


def to_report_settings(settings: SettingsSchema) -> ReportSettings:
    return ReportSettings(
        ate_unit_is_mm=settings.ate_in_mm, directed_ate=settings.directed_ate
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
