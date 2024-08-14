"""This module contains general utility functionality for the aqudem library."""
from typing import List, Any, Callable, Dict

import numpy as np
import static_frame as sf

BUG_REPORT_CTA = "This is most likely a bug. Please report the issue."


class Error(Exception):  # will be used as aqudem.Error
    """Base class for all of this library's exceptions."""


class XESMissingTraceNameAttribute(Error):
    """The trace needs to be named."""


class XESSamplingFreqError(Error):
    """The trace is missing the sampling frequency or there is an inconsistency."""


class XESMissingTimestamp(Error):
    """An event is missing the timestamp attribute."""


class XESMissingActivityName(Error):
    """An event is missing the activity name attribute."""


class XESMissingActivityInstance(Error):
    """An event is missing the activity instance attribute."""


class XESIncorrectLifecycleTransitionError(Error):
    """The lifecycle transition is not correct."""


def _validate_xes_dataframe_before_processing(xes_ground_truth: sf.FrameHE,
                                              xes_detected: sf.FrameHE) -> None:
    """Check if the XES logs are in a valid format.

    :param xes_ground_truth: The ground truth XES log.
    :param xes_detected: The detected XES log.
    :returns: None"""
    if ("case:sampling_freq" not in xes_detected.columns
        or xes_detected["case:sampling_freq"].count(unique=True) != 1):
        raise XESSamplingFreqError("All XES traces in the log must have "
                                   "a 'sampling_freq' attribute.")
    for xes_frame in [xes_ground_truth, xes_detected]:
        if ("case:concept:name" not in xes_frame.columns
            or xes_frame["case:concept:name"].isna().any()):
            raise XESMissingTraceNameAttribute("The trace must have a name.")
        if ("lifecycle:transition" not in xes_frame.columns
            or not xes_frame["lifecycle:transition"].isin(["complete", "start"]).all()
            or (len(xes_frame.loc[xes_frame["lifecycle:transition"] == "start"])
                != len(xes_frame.loc[xes_frame["lifecycle:transition"] == "complete"]))):
            raise XESIncorrectLifecycleTransitionError(
                "Each activity instance must have an event with a lifecycle transition"
                " from start to complete."
            )
        if ("time:timestamp" not in xes_frame.columns
            or xes_frame["time:timestamp"].isna().any()):
            raise XESMissingTimestamp("Each event must have a timestamp attribute.")
        if ("concept:name" not in xes_frame.columns
            or xes_frame["concept:name"].isna().any()):
            raise XESMissingActivityName("Each event must have an activity name attribute.")


def _validate_xes_dataframe_after_processing(xes_ground_truth: sf.FrameHE,
                                             xes_detected: sf.FrameHE) -> None:
    """ make sure that for each case-activity,
    the "lifecycle:transition" is always first 'start', then 'complete' """
    if (len(xes_detected["case:sampling_freq"].unique()) != 1
        or xes_detected["case:sampling_freq"].isna().any()):
        raise XESSamplingFreqError("The 'sampling_freq' attribute must have the same value for "
                                   "all traces in the detected log.")
    for xes_frame in [xes_ground_truth, xes_detected]:
        for case_id in xes_frame["case:concept:name"].unique():
            case = xes_frame.loc[xes_frame["case:concept:name"] == case_id]
            for activity_name in case["concept:name"].unique():
                activity = case.loc[case["concept:name"] == activity_name]
                current = "complete"
                for transition in activity["lifecycle:transition"].values:
                    if current == "complete" and transition == "start":
                        current = "start"
                    elif current == "start" and transition == "complete":
                        current = "complete"
                    else:
                        raise XESIncorrectLifecycleTransitionError(
                            "Each activity instance must have an event with a lifecycle transition"
                            " from start to complete."
                        )


def _validate_activity_name(event_log1_fr: sf.FrameHE,
                            event_log2_fr: sf.FrameHE,
                            activity_name: str) -> None:
    """Check if the activity name is in the event log.

    :param  event_log1_fr: The event log.
    :param  event_log2_fr: The event log.
    :param activity_name: The name of the activity to validate.
    :returns: None
    """
    if ((activity_name not in event_log1_fr["concept:name"].unique()
         and activity_name not in event_log2_fr["concept:name"].unique())
        and activity_name != "*"):
        raise ValueError(f"The activity name '{activity_name}' is not in the event logs.")


def _validate_case_id(event_log1_fr: sf.FrameHE,
                      event_log2_fr: sf.FrameHE,
                      case_id: str) -> None:
    """Check if the case ID is in the event log.

    :param event_log1_fr: The event log.
    :param event_log2_fr: The event log.
    :param str case_id: The case ID to validate.
    :returns: None
    """
    if ((case_id not in event_log1_fr["case:concept:name"].unique()
         or case_id not in event_log2_fr["case:concept:name"].unique())
        and case_id != "*"):
        raise ValueError(f"The case ID '{case_id}' is not in the event logs.")


def _logs_contain_at_most_one_case_id(event_log_one: sf.FrameHE,
                                      event_log_two: sf.FrameHE) -> bool:
    """Check if the event logs contains only one case ID.

    :param event_log_one: The event log.
    :param event_log_two: The event log.
    :returns: True if the event log contains only one case ID, False otherwise.
    :rtype: bool
    """
    all_case_names = (list(event_log_one["case:concept:name"].values)
                      + list(event_log_two["case:concept:name"].values))
    all_case_names = list(set(all_case_names))
    return len(all_case_names) == 0 or len(all_case_names) == 1


def _logs_contain_at_most_one_activity(event_log_one: sf.FrameHE,
                                       event_log_two: sf.FrameHE) -> bool:
    """Check if the event logs contain only one activity.

    :param event_log_one: The event log.
    :param event_log_two: The event log.
    :param str activity_name: The name of the activity to check for.
    :returns: True if the event logs contain only one activity, False otherwise.
    :rtype: bool
    """
    all_activity_names = (list(event_log_one["concept:name"].values)
                          + list(event_log_two["concept:name"].values))
    all_activity_names = list(set(all_activity_names))
    return len(all_activity_names) == 0 or len(all_activity_names) == 1


def _has_all_required_columns(event_log: sf.FrameHE) -> bool:
    """Check if the event log has all required columns.

    The required columns are ["case:concept:name", "concept:name",
    "lifecycle:transition", "time:timestamp"].
    :param event_log: The event log .
    :returns: True if the event log has all required columns, False otherwise.
    :rtype: bool
    """
    required_columns = ["case:concept:name", "concept:name",
                        "lifecycle:transition", "time:timestamp"]
    return all(col in list(event_log.columns) for col in required_columns)


def _case_activity_level_metric_pre_check(event_log_one: sf.FrameHE,
                                          event_log_two: sf.FrameHE) -> None:
    """Check if the event logs are in a valid format for case and activity level metrics.

    :param event_log_one: The event log.
    :param event_log_two: The event log.
    :param str activity_name: The name of the activity to validate.
    :param str case_id: The case ID to validate.
    :returns: None
    """
    if not _has_all_required_columns(event_log_one) or not _has_all_required_columns(event_log_two):
        raise ValueError(f"The event logs are missing required columns. {BUG_REPORT_CTA}")
    if not _logs_contain_at_most_one_case_id(event_log_one, event_log_two):
        raise ValueError(f"The event logs must contain exactly one case ID. {BUG_REPORT_CTA}")
    if not _logs_contain_at_most_one_activity(event_log_one, event_log_two):
        raise ValueError(f"The event logs must contain exactly one activity type. {BUG_REPORT_CTA}")


def _case_level_metric_pre_check(event_log_one: sf.FrameHE,
                                 event_log_two: sf.FrameHE) -> None:
    """Check if the event logs are in a valid format for case level metrics.

        :param event_log_one: The event log.
        :param event_log_two: The event log.
        :returns: None
        """
    if not _has_all_required_columns(event_log_one) or not _has_all_required_columns(event_log_two):
        raise ValueError(f"The event logs are missing required columns. {BUG_REPORT_CTA}")
    if not _logs_contain_at_most_one_case_id(event_log_one, event_log_two):
        raise ValueError(f"The event logs must contain exactly one case ID. {BUG_REPORT_CTA}")


def _determine_start_end_per_case(gt: sf.FrameHE,
                                  det: sf.FrameHE) -> sf.SeriesHE[sf.Index[np.str_], Any]:
    """Determine the start and end time per case.

    :param gt: The ground truth event log.
    :param det: The detected event log.
    :returns: A dictionary with the case ID as key and a tuple with the start and end time as value.
    """
    start_end_dict = {}
    for case_id in gt["case:concept:name"].unique():
        gt_case = gt.loc[gt["case:concept:name"] == case_id]
        det_case = det.loc[det["case:concept:name"] == case_id]
        if len(gt_case) == 0 or len(det_case) == 0:
            raise ValueError(f"Case ID '{case_id}' is not in both logs. "
                             "Currently, all case IDs must be in both logs. "
                             "Please clean logs before proceeding.")
        start_time = min(gt_case["time:timestamp"].min(), det_case["time:timestamp"].min())
        end_time = max(gt_case["time:timestamp"].max(), det_case["time:timestamp"].max())
        start_end_dict[case_id] = (start_time, end_time)
    return sf.SeriesHE.from_dict(start_end_dict)


# pylint: disable=too-many-arguments, too-many-locals
def _generate_activity_metric_list(gt: sf.FrameHE,
                                   det: sf.FrameHE,
                                   case_id: str,
                                   activity_name: str,
                                   start_end_per_case: sf.SeriesHE[sf.Index[np.str_], Any],
                                   metric: Callable[[sf.FrameHE,
                                                     sf.FrameHE,
                                                     sf.SeriesHE,
                                                     float], Any],
                                   sampling_freq: float = -1.0) -> List[Any]:
    """ Generate a list of metrics for a given case and activity.

    :param gt: The ground truth log.
    :param det: The detected log.
    :param case_id: The case ID.
        If "*" is passed, the metric will be calculated and averaged for all
            case IDs.
    :param activity_name: The name of the activity.
        If "*" is passed, the metric will be calculated and averaged for all
            activities.
    :param start_end_per_case: The start and end times for each case.
    :param metric: The metric to calculate.
    :param sampling_freq: The sampling frequency of the logs, in Hertz.
    :returns: A list of metrics.
    """
    if not _has_all_required_columns(gt) or not _has_all_required_columns(det):
        raise ValueError("Logs must have columns case:concept:name, "
                         f"concept:name, lifecycle:transition, time:timestamp. {BUG_REPORT_CTA}")
    if case_id == "*":
        relevant_case_ids = list(set((list(gt["case:concept:name"].values)
                                      + list(det["case:concept:name"].values))))
    elif case_id != "*":
        relevant_case_ids = [case_id]
    else:
        raise ValueError(f"Case ID must be '*' or a valid case ID. {BUG_REPORT_CTA}")
    metric_list = []
    for case_name in relevant_case_ids:
        gt_filtered_by_case = gt.loc[gt["case:concept:name"] == case_name]
        det_filtered_by_case = det.loc[det["case:concept:name"] == case_name]
        if activity_name == "*":
            relevant_activity_names = list(
                set((list(gt_filtered_by_case["concept:name"].values)
                     + list(det_filtered_by_case["concept:name"].values))))
        elif activity_name != "*":
            relevant_activity_names = [activity_name]
        else:
            raise ValueError("Activity name must be '*' or a valid activity name. "
                             f"{BUG_REPORT_CTA}")
        for act_name in relevant_activity_names:
            gt_filtered_by_activity = gt_filtered_by_case.loc[gt_filtered_by_case[
                                                                  "concept:name"]
                                                              == act_name]
            det_filtered_by_activity = det_filtered_by_case.loc[det_filtered_by_case[
                                                                    "concept:name"]
                                                                == act_name]
            if len(gt_filtered_by_activity) == 0 and len(det_filtered_by_activity) == 0:
                continue
            metric_list.append(metric(gt_filtered_by_activity,
                                      det_filtered_by_activity,
                                      start_end_per_case,
                                      sampling_freq))
    if len(metric_list) == 0:
        raise ValueError(
            "No metrics could be calculated for this combination of case ID(s) and activity name("
            "s).")
    return metric_list


def _generate_sequence_metric_list(gt: sf.FrameHE,
                                   det: sf.FrameHE,
                                   case_id: str,
                                   metric: Callable[[sf.FrameHE,
                                                     sf.FrameHE], Any], ) -> List[Any]:
    """ Generate a list of sequence metrics for a given case.

    :param gt: The ground truth log.
    :param det: The detected log.
    :param case_id: The case ID to calculate the metric for.
        If "*" is passed, the metric will be calculated and averaged for all
            case IDs.
    :param metric: The metric to calculate.
    :returns: A list of metrics.
    """
    if not _has_all_required_columns(gt) or not _has_all_required_columns(det):
        raise ValueError("Logs must have columns case:concept:name, "
                         f"concept:name, lifecycle:transition, time:timestamp. {BUG_REPORT_CTA}")
    if case_id == "*":
        relevant_case_ids = list(set((list(gt["case:concept:name"].values)
                                      + list(det["case:concept:name"].values))))
    elif case_id != "*":
        relevant_case_ids = [case_id]
    else:
        raise ValueError(f"Case ID must be '*' or a valid case ID. {BUG_REPORT_CTA}")
    metric_list = []
    for case_name in relevant_case_ids:
        gt_filtered_by_case = gt.loc[gt["case:concept:name"] == case_name]
        det_filtered_by_case = det.loc[det["case:concept:name"] == case_name]
        if len(gt_filtered_by_case) == 0 and len(det_filtered_by_case) == 0:
            continue
        metric_list.append(metric(gt_filtered_by_case,
                                  det_filtered_by_case))
    return metric_list


def _count_values(input_frame: sf.FrameHE, column: str) -> Dict[Any, int]:
    """Count the number of unique values in a Series.

    :param input_frame: The input Series.
    :returns: A Series with the unique values as index and the count as values.
    """
    # Iterate over the rows of the input FrameHE and count the values
    # for the given column
    value_counts = {}
    for value in input_frame[column].values:
        if value not in value_counts:
            value_counts[value] = 1
        else:
            value_counts[value] += 1
    return value_counts


def _remove_events_with_length_zero(log: sf.FrameHE) -> sf.FrameHE:
    """Remove events with a duration of zero.

    :param log: The event log.
    :returns: The event log without events with a duration of zero.
    """
    case_activity_timestamp_combinations_to_remove = []
    for case_id in log["case:concept:name"].unique():
        case = log.loc[log["case:concept:name"] == case_id]
        for activity_name in case["concept:name"].unique():
            activity = case.loc[case["concept:name"] == activity_name]
            value_counts = _count_values(activity, "time:timestamp")
            keys = [key for key, value in value_counts.items() if value > 1]
            if len(keys) == 0:
                continue
            case_activity_timestamp_combinations_to_remove.extend(
                [(case_id, activity_name, key) for key in keys])
    if len(case_activity_timestamp_combinations_to_remove) == 0:
        return log
    for case_id, activity_name, timestamp in case_activity_timestamp_combinations_to_remove:
        log = log.loc[~((log["case:concept:name"] == case_id)
                        & (log["concept:name"] == activity_name)
                        & (log["time:timestamp"] == timestamp))]
    return log


def _get_case_in_filtered_logs(gt: sf.FrameHE, det: sf.FrameHE) -> str:
    """Get the case ID in the filtered logs.

    :param gt: The ground truth log.
    :param det: The detected log.
    :returns: None
    """

    if len(gt) > 0:
        case_id = str(gt["case:concept:name"].iloc[0])
    elif len(det) > 0:
        case_id = str(det["case:concept:name"].iloc[0])
    else:
        raise ValueError("Both logs, gt and det, are empty. "
                         f"Cannot calculate EA metrics. {BUG_REPORT_CTA}")
    return case_id
