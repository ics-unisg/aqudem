"""Main module."""
from functools import cached_property, lru_cache
from typing import Tuple, Union
import pm4py  # type: ignore
import static_frame as sf
from .two_set_helper import TwoSet
from .utils import (_validate_xes_dataframe_before_processing, _validate_activity_name,
                    _validate_case_id, _determine_start_end_per_case,
                    _remove_events_with_length_zero, _validate_xes_dataframe_after_processing)
from .damerau_levenshtein_helper import (_damerau_levenshtein_distancy_by_case,
                                         _levenshtein_distancy_by_case)
from .cross_correlation_helper import _cross_correlation_by_activity_case
from .two_set_helper import _two_set_by_activity_case
from .event_analysis_helper import (_event_analysis_by_activity_case, EventAnalysis)


class Context:
    """Class that offers main functionality of AquDeM.

    Both files are expected to be in the XES format, with special constraints:
    * The log must have an attribute specifying the sampling frequency in hertz
    (key: "sampling_freq") on the trace level (only the detected log).
    * Must use the concept:name,
    lifecycle:transition and time:timestamp standard extensions.
    * Each activity instance must have an event with at least
    the lifecycle transitions tart and complete.
    * In one case, the same activity can only be executed once at a time.

    An ACTIVITY_METRIC is a metric that is calculated for each activity type
    in each case separately.
    For requests that span multiple activities and/or cases, the results
    are aggregated.
    A SEQUENCE_METRIC is a metric that is calculated for each
    case separately.
    For requests that span multiple cases, the results are aggregated.

    :param str ground_truth: The ground truth log file path.
    :param str detected: The detected log file path.
    :return: An aqudem context instance,
    representing the comparison of two logs.
    """

    def __init__(self, ground_truth: str, detected: str):
        """Initialize the context with the ground truth and detected logs."""
        base_gt = sf.FrameHE.from_pandas(
            pm4py.read_xes(ground_truth).sort_values(by="time:timestamp"))
        base_det = sf.FrameHE.from_pandas(
            pm4py.read_xes(detected).sort_values(by="time:timestamp"))
        _validate_xes_dataframe_before_processing(base_gt, base_det)
        self._ground_truth = _remove_events_with_length_zero(base_gt).relabel(sf.IndexAutoFactory)
        self._detected = _remove_events_with_length_zero(base_det).relabel(sf.IndexAutoFactory)
        _validate_xes_dataframe_after_processing(self._ground_truth, self._detected)
        self._sampling_freq: float = self._detected["case:sampling_freq"].iloc[0]
        self._start_end_per_case = _determine_start_end_per_case(self._ground_truth, self._detected)

    @property
    def ground_truth(self) -> sf.FrameHE:
        """Get the ground truth log."""
        return self._ground_truth

    @property
    def detected(self) -> sf.FrameHE:
        """Get the detected log."""
        return self._detected

    @property
    def sampling_freq(self) -> float:
        """Get the sampling frequency of the logs."""
        return self._sampling_freq

    @cached_property
    def activity_names(self) -> dict[str, list[str]]:
        """Extract all the available activity names from the XES logs.

        :return: A dictionary with "ground_truth" and "detected" keys, each
        containing a list of activity names.
        """
        return {
            "ground_truth": list(set(self._ground_truth["concept:name"].values)),
            "detected": list(set(self._detected["concept:name"].values))
        }

    @cached_property
    def case_ids(self) -> dict[str, list[str]]:
        """Extract all the available case IDs from the XES logs.

        :return: A dictionary with "ground_truth" and "detected" keys, each
        containing a list of case IDs.
        """
        return {
            "ground_truth": list(set(self._ground_truth["case:concept:name"].values)),
            "detected": list(set(self._detected["case:concept:name"].values))
        }

    @lru_cache(maxsize=20)
    def cross_correlation(self,
                          activity_name: str = "*",
                          case_id: str = "*") -> Tuple[float, float]:
        """Calculate the cross-correlation between the ground truth and detected logs.

        ACTIVITY_METRIC

        :param activity_name: The name of the activity to calculate the cross-correlation for.
            If "*" is passed, the cross-correlation will be calculated and averaged for all
            activities.
        :param case_id: The case ID to calculate the cross-correlation for.
            If "*" is passed, the cross-correlation will be calculated and averaged for all
            case IDs.
        :return: Tuple; first element: cross-correlation value, between 0 and 1.
            second element: relative shift to achieve maximum cross correlation.
        """
        _validate_activity_name(self._ground_truth,
                                self._detected,
                                activity_name)
        _validate_case_id(self._ground_truth,
                          self._detected,
                          case_id)
        return _cross_correlation_by_activity_case(self._ground_truth,
                                                   self._detected,
                                                   self._sampling_freq,
                                                   activity_name,
                                                   case_id,
                                                   self._start_end_per_case)

    @lru_cache(maxsize=20)
    def two_set(self, activity_name: str = "*", case_id: str = "*") -> TwoSet:
        """Calculate the 2SET metrics for a given activity. Absolute values.

        ACTIVITY_METRIC

        Includes the absolute and rate metrics, for details see the
        TwoSet class documentation.
        For more info on the metrics, refer to the metrics overview and/or:
        J. A. Ward, P. Lukowicz, and H. W. Gellersen, “Performance metrics for
        activity recognition,” ACM Trans. Intell. Syst. Technol., vol. 2, no. 1, pp. 1–23,
        Jan. 2011, doi: 10.1145/1889681.1889687.; 4.1.2

        :param activity_name: The name of the activity to calculate the two-set metrics for.
            If "*" is passed, the two-set metrics will be calculated
            and aggregated for all activities.
        :param case_id: The case ID to calculate the two-set metrics for.
            If "*" is passed, the two-set metrics will be calculated and
            aggregated for all case IDs.
        :return: A data class with the 2SET metrics.
        """
        _validate_activity_name(self._ground_truth,
                                self._detected,
                                activity_name)
        _validate_case_id(self._ground_truth,
                          self._detected,
                          case_id)
        return _two_set_by_activity_case(self._ground_truth,
                                         self._detected,
                                         self._sampling_freq,
                                         activity_name,
                                         case_id,
                                         self._start_end_per_case)


    @lru_cache(maxsize=20)
    def event_analysis(self, activity_name: str = "*", case_id: str = "*") -> EventAnalysis:
        """Calculate the EA metrics.

        ACTIVITY_METRIC

        Includes the absolute and rate metrics, for details see the
        EventAnalysis class documentation.
        For more info on the metrics, refer to the metrics overview and/or:
        J. A. Ward, P. Lukowicz, and H. W. Gellersen, “Performance metrics for
        activity recognition,” ACM Trans. Intell. Syst. Technol., vol. 2, no. 1, pp. 1–23,
        Jan. 2011, doi: 10.1145/1889681.1889687.; 4.2

        :param activity_name: The name of the activity to calculate the event analysis metrics for.
            If "*" is passed, the metrics will be calculated
            and aggregated for all activities.
        :param case_id: The case ID to calculate the event analysis metrics for.
            If "*" is passed, the metrics will be calculated and
            aggregated for all case IDs.
        :return: A data class with the EAD metrics.
        """
        _validate_activity_name(self._ground_truth,
                                self._detected,
                                activity_name)
        _validate_case_id(self._ground_truth,
                          self._detected,
                          case_id)
        return _event_analysis_by_activity_case(self._ground_truth,
                                                self._detected,
                                                activity_name,
                                                case_id,
                                                self._start_end_per_case)

    @lru_cache(maxsize=20)
    def damerau_levenshtein_distance(self, case_id: str = "*") -> Tuple[Union[float, int], float]:
        """Calculate the Damerau-Levenshtein distance between the ground truth and
            detected logs.

        SEQUENCE_METRIC

        Calculates both the absolute distance and the normalized distance.
        Order of activities based on start timestamps.

        :param case_id: The case ID to calculate the Damerau-Levenshtein distance for.
            If "*" is passed, the Damerau-Levenshtein distance will be calculated and
            averaged for all case IDs.
        :return: The Damerau-Levenshtein distance; tuple.
            The first value in the tuple represents the (average) absolute distance.
            The second value in the tuple represents the (average) normalized distance.
        """
        _validate_case_id(self._ground_truth, self._detected, case_id)
        return _damerau_levenshtein_distancy_by_case(
            self._ground_truth, self._detected, case_id)

    @lru_cache(maxsize=20)
    def levenshtein_distance(self, case_id: str = "*") -> Tuple[Union[float, int], float]:
        """Calculate the Levenshtein distance between the ground truth and detected logs.

        SEQUENCE_METRIC

        Calculates both the absolute distance and the normalized distance.
        Order of activities based on start timestamps.

        :param case_id: The case ID to calculate the Levenshtein distance for.
            If "*" is passed, the Levenshtein distance will be
            calculated and averaged for all case IDs.
        :return: The Levenshtein distance; tuple.
            The first value in the tuple represents the (average) absolute distance.
            The second value in the tuple represents the (average) normalized distance.
        """
        _validate_case_id(self._ground_truth, self._detected, case_id)
        return _levenshtein_distancy_by_case(
            self._ground_truth, self._detected, case_id)
