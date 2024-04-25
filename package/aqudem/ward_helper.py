"""Helper functions for metrics from Ward et al; used in event analysis and 2SET."""
from datetime import datetime
from functools import lru_cache
from typing import Union
import static_frame as sf
from numpy import nan
from .utils import BUG_REPORT_CTA

EIGHT_TYPE_MAPPING_P_C_N = {
    (nan, "FP", "TN"): "I",
    (nan, "FP", "FN"): "I",
    (nan, "FN", "TN"): "D",
    (nan, "FN", "FP"): "D",
    (nan, "FP", "TP"): "Oa",
    (nan, "FN", "TP"): "Ua",
    ("TP", "FP", "TP"): "M",
    ("TP", "FN", "TP"): "F",
    ("TN", "FP", "TP"): "Oa",
    ("FN", "FP", "TP"): "Oa",
    ("TN", "FN", "TP"): "Ua",
    ("FP", "FN", "TP"): "Ua",
    ("TN", "FP", "TN"): "I",
    ("FN", "FP", "TN"): "I",
    ("TN", "FP", "FN"): "I",
    ("FN", "FP", "FN"): "I",
    ("TN", "FN", "TN"): "D",
    ("FP", "FN", "TN"): "D",
    ("TN", "FN", "FP"): "D",
    ("FP", "FN", "FP"): "D",
    ("TP", "FP", "TN"): "Oo",
    ("TP", "FP", "FN"): "Oo",
    ("TP", "FN", "TN"): "Uo",
    ("TP", "FN", "FP"): "Uo",
    ("TN", "FP", nan): "I",
    ("FN", "FP", nan): "I",
    ("TN", "FN", nan): "D",
    ("FP", "FN", nan): "D",
    ("TP", "FP", nan): "Oo",
    ("TP", "FN", nan): "Uo"
}

FOUR_TYPE_MAPPING_GT_DET = {
    (True, True): "TP",
    (False, False): "TN",
    (False, True): "FP",
    (True, False): "FN"
}


def _generate_eight_type(prev_type: Union[str, None],
                         segment_type: str,
                         next_type: Union[str, None]) -> str:
    """Generate the eight type of the segment based on the
    type of the segment and the previous and next segment.

    :param str segment_type: The type of the segment.
        In ["TP", "TN", "I", "M", "O", "D", "F", "U"].
    :param str prev_type: The type of the previous segment.
        In ["TP", "TN", "I", "M", "O", "D", "F", "U"].
    :param str next_type: The type of the next segment.
        In ["TP", "TN", "I", "M", "O", "D", "F", "U"].
    :return: The eight type of the segment.
    :rtype: str
    """
    if segment_type not in ["TP", "TN", "FP", "FN"]:
        raise ValueError("The segment type must be 'TP', 'TN', 'FP', or 'FN'.")
    if prev_type not in ["TP", "TN", "FP", "FN", nan]:
        raise ValueError("The previous segment type must be 'TP', 'TN', 'FP', 'FN', or None.")
    if next_type not in ["TP", "TN", "FP", "FN", nan]:
        raise ValueError("The next segment type must be 'TP', 'TN', 'FP', 'FN', or None.")
    if segment_type in ["TP", "TN"]:
        return segment_type
    return EIGHT_TYPE_MAPPING_P_C_N[(prev_type, segment_type, next_type)]


def _is_during_activity_exec(log: sf.FrameHE, timestamp: datetime) -> bool:
    """ Check if the timestamp is during an activity execution.

    Assumes event log to be filtered for certain activity and case.
    Relevant columns/format of the input DataFrames:
    ground_truth:
        - "lifecycle:transition": The lifecycle transition of the event.
        - "time:timestamp": The timestamp of the event, start and complete for all
    :param pd.DataFrame log: The event log.
    :param datetime timestamp: The timestamp to check.
    """
    # check if middle timestamp is during activity in ground truth and detected
    # get the first value with a timestamp smaller than the middle timestamp
    log_before_middle = log.loc[log["time:timestamp"] <= timestamp]
    if len(log_before_middle) == 0:
        return False
    highest_before_middle = log_before_middle.iloc[-1]
    if highest_before_middle["lifecycle:transition"] == "start":
        return True
    if highest_before_middle["lifecycle:transition"] == "complete":
        return False
    raise ValueError("The ground truth log is not in the correct format.")


# pylint: disable=too-many-locals
@lru_cache
def _generate_segment_scores(ground_truth: sf.FrameHE,
                             detected: sf.FrameHE,
                             start_time: datetime,
                             end_time: datetime) -> sf.FrameHE:
    """Generate the segment scores for the ground truth and detected logs.

    Assumes event logs to be filtered for certain activity and case.
    Relevant columns/format of the input DataFrames:
    ground_truth:
        - "lifecycle:transition": The lifecycle transition of the event.
        - "time:timestamp": The timestamp of the event.
    detected:
        - "lifecycle:transition": The lifecycle transition of the event.
        - "time:timestamp": The timestamp of the event.
    Format of the generated DataFrame:
    Columns:
        - "segment_id": The segment ID.
        - "start": The start timestamp of the segment.
        - "end": The end timestamp of the segment.
        - "type": The type of the segment.
            In ["TP", "TN", "I", "M", "Oa", "Oo", "D", "F", "Ua", "Uo"].
    :param ground_truth: The ground truth log.
    :param detected: The detected log.
    :param start_time: The start time of the trace/case.
    :param end_time: The end time of the trace/case.
    """
    if len(ground_truth) == 0 and len(detected) == 0:
        return sf.FrameHE(columns=["start", "end", "type"])
    # Filter the logs to only contain the start and complete events
    ground_truth_filtered: sf.FrameHE = ground_truth.loc[
        ground_truth["lifecycle:transition"].isin(["start", "complete"])] # type: ignore
    detected_filtered = detected.loc[detected["lifecycle:transition"].isin(["start", "complete"])]
    # merge the logs and extract list so that
    # every start and complete event are turned into a boundary
    merged = sf.FrameHE.from_concat([ground_truth_filtered, detected_filtered],
                                    index=sf.IndexAutoFactory,
                                    axis=0)
    merged = merged.sort_values("time:timestamp")
    boundary_timestamps = list(set(list(merged["time:timestamp"].values)))
    boundary_timestamps.sort()
    if start_time < boundary_timestamps[0]:
        boundary_timestamps.insert(0, start_time)
    elif start_time > boundary_timestamps[0]:
        raise ValueError(f"Internal value error regarding timing. {BUG_REPORT_CTA}")
    if end_time > boundary_timestamps[-1]:
        boundary_timestamps.append(end_time)
    elif end_time < boundary_timestamps[-1]:
        raise ValueError(f"Internal value error regarding timing. {BUG_REPORT_CTA}")
    # create a new Dataframe with columns start, end, type
    segment_scores_list = []
    # make sure that the boundary timestamps are in the correct order
    if boundary_timestamps != sorted(boundary_timestamps):
        raise ValueError(f"The boundary timestamps are not in the correct order. {BUG_REPORT_CTA}")
    # iterate over the boundary timestamps and create the segments
    current_type = "None"
    for segment in range(len(boundary_timestamps) - 1):
        start = boundary_timestamps[segment]
        end = boundary_timestamps[segment + 1]
        # get the middle timestamp of the segment
        middle = start + (end - start) / 2
        gt_is_active = _is_during_activity_exec(ground_truth_filtered, middle)
        det_is_active = _is_during_activity_exec(detected_filtered, middle) # type: ignore
        segment_type = FOUR_TYPE_MAPPING_GT_DET[(gt_is_active, det_is_active)]
        # append the segment to the segment_scores DataFrame
        prior_type = current_type
        current_type = segment_type
        if prior_type == current_type:
            raise ValueError(f"The current and prior segment types are the same. {BUG_REPORT_CTA}")
        segment_scores_list.append({"start": start, "end": end, "type": segment_type})
    segment_scores_frame = sf.FrameHE.from_dict_records(segment_scores_list)
    # sort the segment_scores DataFrame by the start timestamp
    segment_scores_frame = segment_scores_frame.sort_values("start")
    # extend the dataframe so that for every row there are new columns
    # prev_type and next_type based on the type of the previous and next segment
    segment_scores_frame = (
        sf.FrameHE.from_concat([segment_scores_frame, segment_scores_frame["type"].shift(1)],
                               axis=1,
                               columns=['start', 'end', 'type', 'prev_type']))
    segment_scores_frame = (
        sf.FrameHE.from_concat([segment_scores_frame, segment_scores_frame["type"].shift(-1)],
                               axis=1,
                               columns=['start', 'end', 'type', 'prev_type', 'next_type']))
    # generate new column eight_type based on the type
    # of the segment and the previous and next segment
    eight_types = (
        segment_scores_frame.iter_series(axis=1).apply(
            lambda x: _generate_eight_type(x["prev_type"], x["type"], x["next_type"])))
    segment_scores_frame = (
        sf.FrameHE.from_concat([segment_scores_frame, eight_types],
                               axis=1,
                               columns=['start', 'end', 'type', 'prev_type',
                                        'next_type', 'eight_type']))
    # remove type, prev_type, and next_type columns
    segment_scores_frame = segment_scores_frame.drop[["type", "prev_type", "next_type"]]
    # rename the eight_type column to type
    segment_scores_frame = segment_scores_frame.relabel(columns=['start', 'end', 'type'])
    return segment_scores_frame
