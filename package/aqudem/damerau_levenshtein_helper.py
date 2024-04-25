"""Functionality for the calculation of the Damerau-Levenshtein distance."""
from functools import partial
from typing import List, Union, Tuple
import static_frame as sf
import textdistance
from .utils import (_case_level_metric_pre_check, BUG_REPORT_CTA,
                    _generate_sequence_metric_list)


def _map_strings_to_letters(list1: List[str],
                            list2: Union[List[str], None] = None) -> Tuple[str, str]:
    """Create two strings where each letter represents a unique string from the list of strings.

    Example:
    (["i", "think", "i", "am", "think", "think", "am", "i"],
    ["therefore", "therefore", "am", "i", "i", "am", "therefore", "am"])
    -> ("ABACBBCA", "DDCAACDC")
    :param [str] list1: The first list of strings.
    :param [str] list2: The second list of strings.
    :return:
    """
    # Combine the two lists if the second list is provided
    all_strings = list1 + (list2 or [])

    # Create a mapping between unique strings and letters
    unique_strings = sorted(set(all_strings), key=all_strings.index)
    letter_mapping = {string: chr(ord('A') + i) for i, string in enumerate(unique_strings)}

    # Map strings to letters for the first list
    result1 = ''.join(letter_mapping[string] for string in list1)

    # Map strings to letters for the second list (if provided)
    result2 = ''
    if list2 is not None:
        result2 = ''.join(letter_mapping[string] for string in list2)

    return result1, result2


def _damerau_levenshtein_distancy_by_case(gt: sf.FrameHE,
                                          det: sf.FrameHE,
                                          case_id: str) -> Tuple[Union[int, float], float]:
    """Calculate the Damerau-Levenshtein distance between the ground truth and detected logs.

    :param gt: The ground truth log.
    :param det: The detected log.
    :param case_id: The case ID to calculate the Damerau-Levenshtein distance for.
        If "*" is passed, the Damerau-Levenshtein distance will be calculated and averaged for all
            case IDs.
    :return: The Damerau-Levenshtein distance and the normalized Damerau-Levenshtein distance.
    """
    all_d_l_distances = _generate_sequence_metric_list(gt, det, case_id,
                                                       partial(_damerau_opt_levenshtein_dist,
                                                               metr_type="dam_lev"))

    return (round(sum(dl[0] for dl in all_d_l_distances) / len(all_d_l_distances), 4),
            round(sum(dl[1] for dl in all_d_l_distances) / len(all_d_l_distances), 4))


def _levenshtein_distancy_by_case(gt: sf.FrameHE,
                                  det: sf.FrameHE,
                                  case_id: str) -> Tuple[Union[int, float], float]:
    """Calculate the Levenshtein distance between the ground truth and detected logs.

    :param gt: The ground truth log.
    :param det: The detected log.
    :param case_id: The case ID to calculate the Levenshtein distance for.
        If "*" is passed, the Levenshtein distance will be calculated and averaged for all
            case IDs.
    :return: The Levenshtein distance and the normalized Levenshtein distance.
    """
    all_d_l_distances = _generate_sequence_metric_list(gt, det, case_id,
                                                       partial(_damerau_opt_levenshtein_dist,
                                                               metr_type="lev"))

    return (round(sum(dl[0] for dl in all_d_l_distances) / len(all_d_l_distances), 4),
            round(sum(dl[1] for dl in all_d_l_distances) / len(all_d_l_distances), 4))


def _damerau_opt_levenshtein_dist(gt: sf.FrameHE,
                                  det: sf.FrameHE,
                                  metr_type: str = "dam_lev") -> Tuple[int, float]:
    """Calculate the (normalized) (Damerau-)Levenshtein distance
    between the ground truth and detected logs.

    Sorted based on start time.
    Assume the logs are filtered by case.
    :param gt: The ground truth log. Filtered by case_id.
    :param det: The detected log. Filtered by case_id.
    :return: Tuple of Damerau-Levenshtein distance and normed version.
    """
    _case_level_metric_pre_check(gt, det)
    gt_start_event_fr = (gt.loc[gt["lifecycle:transition"] == "start"]
                         .sort_values("lifecycle:transition"))
    dt_start_event_fr = (det.loc[det["lifecycle:transition"] == "start"]
                         .sort_values("lifecycle:transition"))
    gt_activity_names = list(gt_start_event_fr["concept:name"].values)
    dt_activity_names = list(dt_start_event_fr["concept:name"].values)
    gt_string, dt_string = _map_strings_to_letters(gt_activity_names, dt_activity_names)
    max_len = max(len(gt_string), len(dt_string))
    if max_len == 0:
        return (0, 0.0)
    if metr_type == "lev":
        return (textdistance.levenshtein(gt_string, dt_string),
                textdistance.levenshtein(gt_string, dt_string) / max_len)
    if metr_type == "dam_lev":
        return (textdistance.damerau_levenshtein(gt_string, dt_string),
                textdistance.damerau_levenshtein(gt_string, dt_string) / max_len)
    raise ValueError(f"Type must be 'dam_lev' or 'lev'. {BUG_REPORT_CTA}")
