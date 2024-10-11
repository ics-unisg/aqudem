""" Helper functions to calculate the Event Analysis (EA) metrics. """
#pylint: disable=too-many-statements, too-many-locals, too-many-branches
from dataclasses import dataclass, fields
from collections import Counter
from functools import cached_property, lru_cache
from typing import Union, Any, Dict
import numpy as np
import static_frame as sf

from .utils import (_case_activity_level_metric_pre_check, BUG_REPORT_CTA,
                    _generate_activity_metric_list, _get_case_in_filtered_logs)
from .ward_helper import _generate_segment_scores


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class EventAnalysis:
    """Data class to hold the EA metrics.

    Regarding the ground truth events: d, f, fm, m.
    Regarding both the ground truth and detected events: c.
    Regarding the (d)etected events: md, fmd, fd, id.
    If result of aggregated request, the values represent the average number of events
    over the relevant case-activity pairs.
    Relative metrics are available as properties.

    :param d: Deletions
    :param f: Fragmentations
    :param fm: Fragmentation and merge
    :param m: Merges
    :param c: Correct
    :param md: Merges
    :param fmd: Fragmentation and merge
    :param fd: Fragmentations
    :param id: Insertions
    """
    d: Union[int, float]
    f: Union[int, float]
    fm: Union[int, float]
    m: Union[int, float]
    c: Union[int, float]
    md: Union[int, float]
    fmd: Union[int, float]
    fd: Union[int, float]
    id: Union[int, float]

    @cached_property
    def total_gt_events(self) -> Union[int, float]:
        """Get the total number of ground truth events."""
        return round(self.d + self.f + self.fm + self.m + (self.c / 2), 4)

    @cached_property
    def total_det_events(self) -> Union[int, float]:
        """Get the total number of detected events."""
        return round((self.c / 2) + self.md + self.fmd + self.fd + self.id, 4)

    @cached_property
    def correct_events_per_log(self) -> Union[int, float]:
        """Get the total number of correct events per log."""
        return round(self.c / 2, 4)

    @cached_property
    def dr(self) -> float:
        """Get the deletion rate.
        Ratio of deletions to total ground truth events."""
        return (round(self.d / self.total_gt_events, 4)
                if self.total_gt_events > 0
                else 0)

    @cached_property
    def fr(self) -> float:
        """Get the fragmentation rate.
        Ratio of fragmentations to total ground truth events."""
        return (round(self.f / self.total_gt_events, 4)
                if self.total_gt_events > 0
                else 0)

    @cached_property
    def fmr(self) -> float:
        """Get the fragmentation and merge rate.
        Ratio of fragmentation and merge to total ground truth events."""
        return (round(self.fm / self.total_gt_events, 4)
                if self.total_gt_events > 0
                else 0)

    @cached_property
    def mr(self) -> float:
        """Get the merge rate.
        Ratio of merges to total ground truth events."""
        return (round(self.m / self.total_gt_events, 4)
                if self.total_gt_events > 0
                else 0)

    @cached_property
    def cr_gt(self) -> float:
        """Get the correct rate.
        Ratio of correct events per log to total ground truth events."""
        return (round(self.correct_events_per_log / self.total_gt_events, 4)
                if self.total_gt_events > 0
                else 0)

    @cached_property
    def mdr(self) -> float:
        """Get the merging rate.
        Ratio of merging to total detected events."""
        return (round(self.md / self.total_det_events, 4)
                if self.total_det_events > 0
                else 0)

    @cached_property
    def fmdr(self) -> float:
        """Get the fragmentating and merging rate.
        Ratio of fragmentating and merging to total detected events."""
        return (round(self.fmd / self.total_det_events, 4)
                if self.total_det_events > 0
                else 0)

    @cached_property
    def fdr(self) -> float:
        """Get the fragmentating rate.
        Ratio of fragmentating to total detected events."""
        return (round(self.fd / self.total_det_events, 4)
                if self.total_det_events > 0
                else 0)

    @cached_property
    def idr(self) -> float:
        """Get the insertion rate.
        Ratio of insertion to total detected events."""
        return (round(self.id / self.total_det_events, 4)
                if self.total_det_events > 0
                else 0)

    @cached_property
    def cr_det(self) -> float:
        """Get the correct rate.
        Ratio of correct events per log to total detected events."""
        return (round(self.correct_events_per_log / self.total_det_events, 4)
                if self.total_det_events > 0
                else 0)

    @cached_property
    def true_positives(self) -> Union[int, float]:
        """Get the number of true/correct event detections."""
        return round(self.correct_events_per_log, 4)

    @cached_property
    def false_positives(self) -> Union[int, float]:
        """Get the number of false (not correct) event detections."""
        result  = round(self.md + self.fmd + self.fd + self.id, 4)
        if not abs(result - (self.total_det_events - self.correct_events_per_log)) < 0.01:
            raise ValueError(f"False positives calculation error. "
                             f"{BUG_REPORT_CTA}")
        return result

    @cached_property
    def false_negatives(self) -> Union[int, float]:
        """Get the number of ground truth events that have not been categorized as correct."""
        result = round(self.d + self.f + self.fm + self.m, 4)
        if not abs(result - (self.total_gt_events - self.correct_events_per_log)) < 0.01:
            raise ValueError(f"False negatives calculation error. "
                             f"{BUG_REPORT_CTA}")
        return result


    @cached_property
    def precision(self) -> float:
        """Get the precision.
        Ratio of true positives to all positive predictions."""
        return (round(self.true_positives / (self.true_positives + self.false_positives), 4)
                if self.true_positives + self.false_positives > 0
                else 0)

    @cached_property
    def recall(self) -> float:
        """Get the recall.
        Ratio of true positives to the number of all positives in ground truth."""
        return (round(self.true_positives / (self.true_positives + self.false_negatives), 4)
                if self.true_positives + self.false_negatives > 0
                else 0)

    @cached_property
    def f1(self) -> float:
        """Get the F1 score.
        Harmonic mean of precision and recall."""
        return (round((2 * self.precision * self.recall) / (self.precision + self.recall), 4)
                if self.precision + self.recall > 0
                else 0)


@lru_cache
def _event_analysis(gt: sf.FrameHE,
                    det: sf.FrameHE,
                    start_end_per_case: sf.SeriesHE[sf.Index[np.str_], Any],
                    _: float = -1.0) -> EventAnalysis:
    """Calculate the absolute EA metrics.

    Assume that the logs are filtered by activity and case id.
    :param sf.FrameHE gt: The ground truth event log.
    :param sf.FrameHE det: The detected event log.
    :param start_end_by_case: The start and end times of the cases.
    :return: The absolute EA metrics.
    """
    case_id = _get_case_in_filtered_logs(gt, det)
    _case_activity_level_metric_pre_check(gt, det)
    segment_scores = _generate_segment_scores(gt,
                                              det,
                                              start_end_per_case[case_id][0],
                                              start_end_per_case[case_id][1])
    proc_gt_rows = []
    proc_det_rows = []
    final_gt_rows = []
    final_det_rows = []
    for i in range(0, len(gt), 2):
        if (gt.iloc[i]["lifecycle:transition"] != "start"
            or gt.iloc[i + 1]["lifecycle:transition"] != "complete"):
            raise ValueError(f"Invalid log row ordering. {BUG_REPORT_CTA}")
        event_start = gt.iloc[i]["time:timestamp"]
        event_end = gt.iloc[i + 1]["time:timestamp"]
        proc_gt_rows.append({
            "start": event_start,
            "end": event_end,
            "types": []
        })
    for i in range(0, len(det), 2):
        if (det.iloc[i]["lifecycle:transition"] != "start"
            or det.iloc[i + 1]["lifecycle:transition"] != "complete"):
            raise ValueError(f"Invalid log row ordering. {BUG_REPORT_CTA}")
        event_start = det.iloc[i]["time:timestamp"]
        event_end = det.iloc[i + 1]["time:timestamp"]
        proc_det_rows.append({
            "start": event_start,
            "end": event_end,
            "types": []
        })
    for gt_event in proc_gt_rows:
        contained_segment_scores = segment_scores.loc[
            (segment_scores["start"] >= gt_event["start"])
            & (segment_scores["end"] <= gt_event["end"])]
        equal_segment_scores = segment_scores.loc[
            (segment_scores["start"] == gt_event["start"])
            & (segment_scores["end"] == gt_event["end"])]
        if (len(equal_segment_scores) == 1
            and equal_segment_scores.iloc[0]["type"] == "D"):
            gt_event["types"].append("D")
        elif len(contained_segment_scores.loc[contained_segment_scores["type"] == "F"]) > 0:
            gt_event["types"].append("F")
    for det_event in proc_det_rows:
        contained_segment_scores = segment_scores.loc[
            (segment_scores["start"] >= det_event["start"])
            & (segment_scores["end"] <= det_event["end"])]
        equal_segment_scores = segment_scores.loc[
            (segment_scores["start"] == det_event["start"])
            & (segment_scores["end"] == det_event["end"])]
        if (len(equal_segment_scores) == 1
            and equal_segment_scores.iloc[0]["type"] == "I"):
            det_event["types"].append("I'")
        elif len(contained_segment_scores.loc[contained_segment_scores["type"] == "M"]) > 0:
            det_event["types"].append("M'")
    for gt_event in proc_gt_rows:
        overlapping_det_events = [det_event for det_event in proc_det_rows
                          if (gt_event["end"] >= det_event["start"] >= gt_event["start"])
                          or (gt_event["start"] <= det_event["end"] <= gt_event["end"])
                          or ((det_event["start"] <= gt_event["start"] <= det_event["end"])
                              and (det_event["start"] <= gt_event["end"] <= det_event["end"]))]
        if any("M'" in det_event["types"] for det_event in overlapping_det_events):
            gt_event["types"].append("M")
    for det_event in proc_det_rows:
        overlapping_gt_events = [gt_event for gt_event in proc_gt_rows
                         if (det_event["end"] >= gt_event["start"] >= det_event["start"])
                         or (det_event["start"] <= gt_event["end"] <= det_event["end"])
                         or ((gt_event["start"] <= det_event["start"] <= gt_event["end"])
                             and (gt_event["start"] <= det_event["end"] <= gt_event["end"]))]
        if any("F" in gt_event["types"] for gt_event in overlapping_gt_events):
            det_event["types"].append("F'")
    for gt_event in proc_gt_rows:
        if len(gt_event["types"]) == 0:
            final_gt_rows.append({
                "start": gt_event["start"],
                "end": gt_event["end"],
                "type": "C"
            })
        elif "D" in gt_event["types"]:
            final_gt_rows.append({
                "start": gt_event["start"],
                "end": gt_event["end"],
                "type": "D"
            })
        elif "F" in gt_event["types"] and "M" in gt_event["types"]:
            final_gt_rows.append({
                "start": gt_event["start"],
                "end": gt_event["end"],
                "type": "FM"
            })
        elif "F" in gt_event["types"]:
            final_gt_rows.append({
                "start": gt_event["start"],
                "end": gt_event["end"],
                "type": "F"
            })
        elif "M" in gt_event["types"]:
            final_gt_rows.append({
                "start": gt_event["start"],
                "end": gt_event["end"],
                "type": "M"
            })
    for det_event in proc_det_rows:
        if len(det_event["types"]) == 0:
            final_det_rows.append({
                "start": det_event["start"],
                "end": det_event["end"],
                "type": "C"
            })
        elif "I'" in det_event["types"]:
            final_det_rows.append({
                "start": det_event["start"],
                "end": det_event["end"],
                "type": "I'"
            })
        elif "F'" in det_event["types"] and "M'" in det_event["types"]:
            final_det_rows.append({
                "start": det_event["start"],
                "end": det_event["end"],
                "type": "FM'"
            })
        elif "F'" in det_event["types"]:
            final_det_rows.append({
                "start": det_event["start"],
                "end": det_event["end"],
                "type": "F'"
            })
        elif "M'" in det_event["types"]:
            final_det_rows.append({
                "start": det_event["start"],
                "end": det_event["end"],
                "type": "M'"
            })
    gt_types = Counter(row["type"] for row in final_gt_rows)
    det_types = Counter(row["type"] for row in final_det_rows)
    if gt_types["C"] != det_types["C"]:
        raise ValueError(f"The number of correct events in the ground truth and detected logs "
                         f"must be equal. {BUG_REPORT_CTA}")
    return EventAnalysis(
        d=gt_types["D"],
        f=gt_types["F"],
        fm=gt_types["FM"],
        m=gt_types["M"],
        c=gt_types["C"] + det_types["C"],
        md=det_types["M'"],
        fmd=det_types["FM'"],
        fd=det_types["F'"],
        id=det_types["I'"]
    )


def _event_analysis_by_activity_case(gt: sf.FrameHE,
                                     det: sf.FrameHE,
                                     activity: str,
                                     case_id: str,
                                     start_end_per_case: \
                                        sf.SeriesHE[sf.Index[np.str_], Any]) \
                                            -> EventAnalysis:
    """Calculate the absolute EA metrics for a given activity and case id.

    :param sf.FrameHE gt: The ground truth event log.
    :param sf.FrameHE det: The detected event log.
    :param str activity: The activity name.
        If "*" is passed, the EA rates will be calculated and averaged for all activities.
    :param str case_id: The case id.
        If "*" is passed, the EA rates will be calculated and averaged for all cases.
    :param start_end_per_case: The start and end times of the cases.
    :return: The absolute EA metrics.
    """
    all_metrics = _generate_activity_metric_list(gt=gt,
                                                 det=det,
                                                 case_id=case_id,
                                                 activity_name=activity,
                                                 start_end_per_case=start_end_per_case,
                                                 metric=_event_analysis)
    avg_ea_dict: Dict[str, Union[float, int]]= {
        "d": 0,
        "f": 0,
        "fm": 0,
        "m": 0,
        "c": 0,
        "md": 0,
        "fmd": 0,
        "fd": 0,
        "id": 0
    }
    for ea_metr in all_metrics:
        for field in fields(EventAnalysis):
            avg_ea_dict[field.name] += + getattr(ea_metr, field.name)
    for field in fields(EventAnalysis):
        avg_ea_dict[field.name] = round(avg_ea_dict[field.name] / len(all_metrics), 4)
    return EventAnalysis(**avg_ea_dict)
