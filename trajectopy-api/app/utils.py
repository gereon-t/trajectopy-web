from datetime import datetime, timedelta

import trajectopy as tpy
from app import dtos
from app.repository import models

UNIT_DICT = {"meter": tpy.PairDistanceUnit.METER, "second": tpy.PairDistanceUnit.SECOND}

SESSION_TIMEOUT = timedelta(days=1)


def is_session_expired(session: models.Session) -> bool:
    return (datetime.now() - datetime.strptime(session.date, "%Y-%m-%d %H:%M:%S")) > SESSION_TIMEOUT


def try_local_frame(trajectories: list[tpy.Trajectory]) -> None:
    if len(trajectories) < 2:
        return

    reference_trajectory = next((traj for traj in trajectories if traj.pos.local_transformer is not None), None)

    if reference_trajectory is None:
        return

    for traj in trajectories:
        traj.pos.local_transformer = reference_trajectory.pos.local_transformer
        traj.pos.to_local()


def create_plot_report(trajectories: list[tpy.Trajectory], settings: dtos.SettingsDTO):
    report_settings = to_report_settings(settings)

    try_local_frame(trajectories)

    return tpy.create_trajectory_report(trajectories=trajectories, report_settings=report_settings)


def create_comparison_report(gt_traj: tpy.Trajectory, est_traj: tpy.Trajectory, settings: dtos.SettingsDTO):
    processing_settings = to_processing_settings(settings)
    report_settings = to_report_settings(settings)

    try_local_frame([gt_traj, est_traj])

    ate_result = tpy.ate(trajectory_gt=gt_traj, trajectory_est=est_traj, settings=processing_settings)
    rpe_result = (
        tpy.rpe(trajectory_gt=gt_traj, trajectory_est=est_traj, settings=processing_settings)
        if settings.rpe_enabled
        else None
    )

    return tpy.create_deviation_report(ate_result=ate_result, rpe_result=rpe_result, report_settings=report_settings)


def to_alignment_estimation_settings(
    settings: dtos.SettingsDTO,
) -> tpy.AlignmentEstimationSettings:
    return tpy.AlignmentEstimationSettings(
        trans_x=settings.similarity_transformation,
        trans_y=settings.similarity_transformation,
        trans_z=settings.similarity_transformation,
        rot_x=settings.similarity_transformation,
        rot_y=settings.similarity_transformation,
        rot_z=settings.similarity_transformation,
        scale=settings.scale_estimation,
        lever_x=settings.lever_arm_estimation,
        lever_y=settings.lever_arm_estimation,
        lever_z=settings.lever_arm_estimation,
        time_shift=settings.time_shift_estimation,
        sensor_rotation=settings.sensor_rotation_estimation,
    )


def to_relative_comparison_settings(
    settings: dtos.SettingsDTO,
) -> tpy.RelativeComparisonSettings:
    return tpy.RelativeComparisonSettings(
        pair_min_distance=settings.rpe_min_distance,
        pair_max_distance=settings.rpe_max_distance,
        pair_distance_step=settings.rpe_distance_step,
        pair_distance_unit=UNIT_DICT[settings.rpe_distance_unit],
        use_all_pose_pairs=settings.rpe_use_all_pairs,
    )


def to_processing_settings(settings: dtos.SettingsDTO) -> tpy.ProcessingSettings:
    alignment_settings = tpy.AlignmentSettings(estimation_settings=to_alignment_estimation_settings(settings))
    relative_comparison_settings = to_relative_comparison_settings(settings)

    return tpy.ProcessingSettings(
        matching=tpy.MatchingSettings(method=tpy.MatchingMethod(settings.matching)),
        alignment=alignment_settings,
        relative_comparison=relative_comparison_settings,
    )


def to_report_settings(settings: dtos.SettingsDTO) -> tpy.ReportSettings:
    return tpy.ReportSettings(ate_unit_is_mm=settings.ate_in_mm, directed_ate=settings.directed_ate)
