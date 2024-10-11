"""Module to calculate the 2SET metrics."""
from dataclasses import dataclass, fields
from datetime import timedelta
from functools import cached_property, lru_cache
from typing import Union, Any, Dict
import numpy as np
import static_frame as sf
from .ward_helper import _generate_segment_scores
from .utils import (_case_activity_level_metric_pre_check,
                    _generate_activity_metric_list, BUG_REPORT_CTA, _get_case_in_filtered_logs)


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class TwoSet:
    """Data class to hold the 2SET metrics.

    How many of the det frames can be seen as tp, tn, d, f, ua, uo, i, m, oa, oo.
    If result of aggregated request, the values represent the average number of frames
    over the relevant case-activity pairs.
    Relative metrics are available as properties.

    :param tp: True Positives
    :param tn: True Negatives
    :param d: Deletions
    :param f: Fragmentations
    :param ua: Underfullings (at the start)
    :param uo: Underfullings (at the end)
    :param i: Insertions
    :param m: Merges
    :param oa: Overfullings (at the start)
    :param oo: Overfullings (at the end)
    """
    tp: Union[int, float]
    tn: Union[int, float]
    d: Union[int, float]
    f: Union[int, float]
    ua: Union[int, float]
    uo: Union[int, float]
    i: Union[int, float]
    m: Union[int, float]
    oa: Union[int, float]
    oo: Union[int, float]

    @cached_property
    def p(self) -> Union[int, float]:
        """Get total positive frame number in ground truth."""
        return self.tp + self.d + self.f + self.ua + self.uo

    @cached_property
    def p_det(self) -> Union[int, float]:
        """Get total positive frame number in detection."""
        return self.tp + self.i + self.m + self.oa + self.oo

    @cached_property
    def n(self) -> Union[int, float]:
        """Get total negative frames in ground truth."""
        return self.tn + self.i + self.m + self.oa + self.oo

    @cached_property
    def n_det(self) -> Union[int, float]:
        """Get total negative frames in detection."""
        return self.tn + self.d + self.f + self.ua + self.uo

    @cached_property
    def t(self) -> Union[int, float]:
        """Get total frames."""
        return (self.tp + self.tn + self.d + self.f + self.ua
                + self.uo + self.i + self.m + self.oa + self.oo)

    @cached_property
    def tpr(self) -> float:
        """Get the True Positive Rate.
        Ratio of true positives to total positives.

        Equivalent to recall. Left for compatibility."""
        return self.recall

    @cached_property
    def tnr(self) -> float:
        """Get the True Negative Rate.
        Ratio of true negatives to total negatives."""
        return round(self.tn / self.n if self.n != 0 else 0, 4)

    @cached_property
    def dr(self) -> float:
        """Get the Deletion Rate.
        Ratio of deletions to total positives."""
        return round(self.d / self.p if self.p != 0 else 0, 4)

    @cached_property
    def fr(self) -> float:
        """Get the Fragmentation Rate.
        Ratio of fragmentations to total positives."""
        return round(self.f / self.p if self.p != 0 else 0, 4)

    @cached_property
    def uar(self) -> float:
        """Get the Underfilling Rate (at the start).
        Ratio of underfullings at the start to total positives."""
        return round(self.ua / self.p if self.p != 0 else 0, 4)

    @cached_property
    def uor(self) -> float:
        """Get the Underfilling Rate (at the end).
        Ratio of underfullings at the end to total positives."""
        return round(self.uo / self.p if self.p != 0 else 0, 4)

    @cached_property
    def ir(self) -> float:
        """Get the Insertion Rate.
        Ratio of insertions to total negatives."""
        return round(self.i / self.n if self.n != 0 else 0, 4)

    @cached_property
    def mr(self) -> float:
        """Get the Merge Rate.
        Ratio of merges to total negatives."""
        return round(self.m / self.n if self.n != 0 else 0, 4)

    @cached_property
    def oar(self) -> float:
        """Get the Overfilling Rate (at the start).
        Ratio of overfullings at the start to total negatives."""
        return round(self.oa / self.n if self.n != 0 else 0, 4)

    @cached_property
    def oor(self) -> float:
        """Get the Overfilling Rate (at the end).
        Ratio of overfullings at the end to total negatives."""
        return round(self.oo / self.n if self.n != 0 else 0, 4)

    @cached_property
    def precision(self) -> float:
        """Get the precision.
        Ratio of true positives to total positive detections."""
        return round(self.tp / self.p_det if self.p_det != 0 else 0, 4)

    @cached_property
    def recall(self) -> float:
        """Get the recall.
        Ratio of true positives to total positives in ground truth."""
        return round(self.tp / self.p if self.p != 0 else 0, 4)

    @cached_property
    def f1(self) -> float:
        """Get the F1 score.
        Harmonic mean of precision and recall."""
        return round(2 * (self.precision * self.recall) / (self.precision + self.recall)
                     if self.precision + self.recall != 0 else 0, 4)

    @cached_property
    def balanced_accuracy(self) -> float:
        """Get the balanced accuracy.
        Average of true positive rate and true negative rate."""
        return round((self.tpr + self.tnr) / 2, 4)



# pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements
@lru_cache
def _two_set(gt: sf.FrameHE,
             det: sf.FrameHE,
             start_end_by_case: sf.SeriesHE[sf.Index[np.str_], Any],
             sampling_freq: float,) -> TwoSet:
    """Calculate the absolute 2SET metrics.

    Assume that logs are filtered by case and activity.
    :param gt: The ground truth DataFrame.
    :param det: The detected DataFrame.
    :param sampling_freq: The sampling frequency of the logs, in Hz.
    :param start_end_by_case: The start and end times for each case.
    :return: The absolute 2SET metrics.
    """
    case_id = _get_case_in_filtered_logs(gt, det)
    _case_activity_level_metric_pre_check(gt, det)
    sampling_timedelta = timedelta(seconds=1 / sampling_freq)
    segment_scores_frame = _generate_segment_scores(gt,
                                                    det,
                                                    start_end_by_case[case_id][0],
                                                    start_end_by_case[case_id][1])
    sorted_segments_scores_frame = segment_scores_frame.sort_values("start")
    # initialize the counters
    tp = 0
    tn = 0
    d = 0
    f = 0
    ua = 0
    uo = 0
    i = 0
    m = 0
    oa = 0
    oo = 0
    # iterate through the time represented in the segment df
    current_time = sorted_segments_scores_frame.iloc[0]["start"]
    while True:
        current_segment = sorted_segments_scores_frame.loc[
            sorted_segments_scores_frame["start"] <= current_time].iloc[-1]
        if len(current_segment) == 0:
            raise ValueError(f"No segment found for the current time. {BUG_REPORT_CTA}")
        if len(current_segment) > 1 and not isinstance(current_segment, sf.Series):
            raise ValueError("Multiple segments found for the current time. "
                             f"{BUG_REPORT_CTA}")
        # get the type of the current segment
        current_type = current_segment.loc["type"]
        # update the counters
        if current_type == "TP":
            tp += 1
        elif current_type == "TN":
            tn += 1
        elif current_type == "D":
            d += 1
        elif current_type == "F":
            f += 1
        elif current_type == "Ua":
            ua += 1
        elif current_type == "Uo":
            uo += 1
        elif current_type == "I":
            i += 1
        elif current_type == "M":
            m += 1
        elif current_type == "Oa":
            oa += 1
        elif current_type == "Oo":
            oo += 1
        # move to the next time
        current_time += sampling_timedelta
        # if the current time is larger than the last segment, break the loop
        if current_time > sorted_segments_scores_frame.iloc[-1]["end"]:
            break
    return TwoSet(tp=tp, tn=tn, d=d, f=f, ua=ua, uo=uo, i=i, m=m, oa=oa, oo=oo)


def _two_set_by_activity_case(gt: sf.FrameHE,
                              det: sf.FrameHE,
                              sampling_freq: float,
                              activity_name: str,
                              case_id: str,
                              start_end_per_case: sf.SeriesHE[sf.Index[np.str_], Any]) \
                                -> TwoSet:
    """Calculate the absolute 2SET metrics for a given activity and case.

    :param gt: The ground truth log.
    :param det: The detected log.
    :param activity_name: The name of the activity.
        If "*" is passed, the 2SET metrics will be calculated
        and averaged for all activities.
    :param case_id: The case ID.
        If "*" is passed, the 2SET metrics will be calculated
        and averaged for all cases.
    :param start_end_per_case: The start and end times for each case.
    :return: The absolute 2SET metrics.
    """
    two_set_metrics = _generate_activity_metric_list(gt=gt,
                                                     det=det,
                                                     sampling_freq=sampling_freq,
                                                     case_id=case_id,
                                                     activity_name=activity_name,
                                                     start_end_per_case=start_end_per_case,
                                                     metric=_two_set)
    avg_two_set_dict: Dict[str, Union[float, int]] = {
        "tp": 0,
        "tn": 0,
        "d": 0,
        "f": 0,
        "ua": 0,
        "uo": 0,
        "i": 0,
        "m": 0,
        "oa": 0,
        "oo": 0
    }
    for two_set_metr in two_set_metrics:
        for field in fields(TwoSet):
            avg_two_set_dict[field.name] += getattr(two_set_metr, field.name)
    for field in fields(TwoSet):
        avg_two_set_dict[field.name] = round(avg_two_set_dict[field.name]
                                             / len(two_set_metrics), 4)
    return TwoSet(**avg_two_set_dict)
