""" This module contains the cross correlation helper functions. """
import math
from datetime import datetime, timedelta
from typing import List, Tuple, Any
import static_frame as sf
import numpy as np
from .utils import _generate_activity_metric_list


# pylint: disable=too-many-arguments
def _cross_correlation_by_activity_case(ground_truth: sf.FrameHE,
                                        detected: sf.FrameHE,
                                        sampling_freq: float,
                                        activity_name: str,
                                        case_id: str,
                                        start_end_per_case: \
                                            sf.SeriesHE[sf.Index[np.str_], Any]) \
                                                -> Tuple[float, float]:
    """Calculate the cross correlation between the ground truth and detected logs.

    :param ground_truth: The ground truth log.
    :param detected: The detected log.
    :param sampling_freq: The sampling frequency of the logs, in Hertz.
    :param activity_name: The name of the activity.
        If "*" is passed, the cross-correlation will be calculated and averaged for all activities.
    :param case_id: The case ID.
           If "*" is passed, the cross-correlation will be calculated and averaged for all case IDs.
    :param start_end_per_case: The start and end times for each case.
    :return: The cross correlation.
    """
    cross_correlations = _generate_activity_metric_list(gt=ground_truth,
                                                        det=detected,
                                                        case_id=case_id,
                                                        activity_name=activity_name,
                                                        start_end_per_case=start_end_per_case,
                                                        metric=_cross_correlation,
                                                        sampling_freq=sampling_freq)
    return (round(sum(cc[0] for cc in cross_correlations) / len(cross_correlations), 4),
            round(sum(cc[1] for cc in cross_correlations) / len(cross_correlations), 4))


def _cross_correlation(gt: sf.FrameHE,
                       det: sf.FrameHE,
                       start_end_per_case: sf.SeriesHE[sf.Index[np.str_], Any],
                       sampling_rate_hz: float) -> Tuple[float, float]:
    """
    Relative shift > 0 -> the detected activity timeseries had
    to be pushed forward in time (time delay/detected later than actual)
    Relative shift < 0 -> the detected activity timeseries had
    to be pulled back (time advance/detected earlier than actual)

    Assume
    :param gt: Ground truth log
    :param det: Detected log
    :param start_end_per_case: Start and end times for all cases
    :param sampling_rate_hz: Sampling rate in Hz
    :return: cross correlation and relative shift necessary for max cc
    """
    if len(gt) == 0 or len(det) == 0:
        return 0.0, 0.0
    time_series_bin_gt, time_series_bin_det = _get_timeseries_format(gt,
                                                                     det,
                                                                     sampling_rate_hz,
                                                                     start_end_per_case)
    a = np.array(time_series_bin_gt)
    b = np.array(time_series_bin_det)
    if len(a) != len(b):
        raise ValueError("Time series must have same length.")
    normalization_factor = len(a)
    c = np.correlate(a, b, mode='full')
    c_max = c.max()
    c_list = list(c)
    if c_max != 0.0:
        c_ind = c_list.index(c_max)
        shift_total = c_ind - math.floor(len(c_list) / 2)
        shift_relative = shift_total / math.floor(len(c_list) / 2)
    else:
        shift_relative = 0.0
    return round(c_max / normalization_factor, 2), round(shift_relative, 2)


def _get_timeseries_format(gt: sf.FrameHE,
                           det: sf.FrameHE,
                           sampling_rate_hz: float,
                           start_end_per_case: sf.SeriesHE[sf.Index[np.str_], Any], ) \
    -> Tuple[List[int], List[int]]:
    """
    Turns a list of ground truth and detected activity
    instances into a time series when the activity is running and
    when not. All activities must be of same type (have same name).
    :param gt:
    :param det:
    :param sampling_rate_hz:
    :return:
    """
    case_id = gt["case:concept:name"].iloc[0]
    sorted_gt = gt.sort_values("time:timestamp")
    sorted_det = det.sort_values("time:timestamp")
    min_start: datetime = start_end_per_case[case_id][0]
    max_stop: datetime = start_end_per_case[case_id][1]
    time_step = timedelta(seconds=1) / sampling_rate_hz
    timeseries_gt = []
    timeseries_det = []

    current_time = min_start
    while current_time <= max_stop:
        rel_rows_gt = sorted_gt.loc[(sorted_gt["time:timestamp"] >= current_time)]
        if len(rel_rows_gt) > 0 and (rel_rows_gt["lifecycle:transition"].
                                         values[0] == "complete"
                                     or (rel_rows_gt["time:timestamp"]
                                             .values[0] == current_time and
                                         rel_rows_gt["lifecycle:transition"]
                                             .values[0] == "start")):
            timeseries_gt.append(1)
        else:
            timeseries_gt.append(-1)
        rel_rows_det = sorted_det.loc[(sorted_det["time:timestamp"] >= current_time)]
        if len(rel_rows_det) > 0 and (rel_rows_det["lifecycle:transition"]
                                          .values[0] == "complete"
                                        or (rel_rows_det["time:timestamp"]
                                                .values[0] == current_time and
                                            rel_rows_det["lifecycle:transition"]
                                                .values[0] == "start")):
            timeseries_det.append(1)
        else:
            timeseries_det.append(-1)
        current_time += time_step
    return timeseries_gt, timeseries_det
