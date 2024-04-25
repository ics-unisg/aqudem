""" Tests for the cross correlation functionality of the aqudem package."""
import os
from unittest.mock import patch, MagicMock
import static_frame
import aqudem
from aqudem.cross_correlation_helper import _cross_correlation, _get_timeseries_format
from .mocks.logs import (basic_mock_gt, basic_mock_det,
                         start_end_series_basic,
                         start_end_series_basic_only_det,
                         basic_mock_gt_1, basic_mock_det_1,
                         start_end_series_basic_1,
                         start_end_series_basic_1_only_det,
                         start_end_series_basic_1_only_gt,
                         basic_mock_gt_2, basic_mock_det_2,
                         start_end_series_basic_2,)

EMPTY_FRAME_HE = static_frame.FrameHE.from_dict({
    "case:concept:name": [],
    "time:timestamp": [],
    "lifecycle:transition": [],
})

def test_get_timeseries_format_basic() -> None:
    res = _get_timeseries_format(basic_mock_gt,
                                 basic_mock_det,
                                 1,
                                 start_end_series_basic)
    assert res[0] == [1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1]
    assert res[1] == [-1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1]

    res = _get_timeseries_format(basic_mock_gt_1,
                                 basic_mock_det_1,
                                 1,
                                 start_end_series_basic_1)
    assert res[0] == [1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
    assert res[1] == [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1]

    res = _get_timeseries_format(basic_mock_gt_2,
                                 basic_mock_det_2,
                                 1,
                                 start_end_series_basic_2)
    assert res[0] == [1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1]
    assert res[1] == [-1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1]

def test_get_timeseries_format_basic_2hz() -> None:
    res = _get_timeseries_format(basic_mock_gt,
                                 basic_mock_det,
                                 2,
                                 start_end_series_basic)
    assert res[0] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      -1, -1, -1, -1, -1, 1, 1, 1, -1, -1]
    assert res[1] == [-1, -1, -1, -1, -1, -1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, -1, -1, -1, 1, 1, 1]

def test_cc_basic() -> None:
    cc = _cross_correlation(basic_mock_gt,
                            basic_mock_det,
                            start_end_series_basic,
                            1)
    assert cc == (0.45, -0.2)


def test_cc_same_seq_returns_1_0() -> None:
    cc = _cross_correlation(basic_mock_det,
                            basic_mock_det,
                            start_end_series_basic_only_det,
                            1)
    assert cc == (1, 0.0)


def test_correct_sign_shift() -> None:
    cc = _cross_correlation(basic_mock_gt_1,
                            basic_mock_det_1,
                            start_end_series_basic_1,
                            1)
    assert cc == (0.55, -0.5)


def test_cc_none() -> None:
    """ Check that empty activity list leads to (None, None) return """
    cc1 = _cross_correlation(EMPTY_FRAME_HE,
                             basic_mock_det_1,
                             start_end_series_basic_1_only_det,
                             1)
    cc2 = _cross_correlation(basic_mock_gt_1,
                             EMPTY_FRAME_HE,
                             start_end_series_basic_1_only_gt,
                             1)
    cc3 = _cross_correlation(EMPTY_FRAME_HE,
                             EMPTY_FRAME_HE,
                             static_frame.SeriesHE.from_dict({}),
                             1)
    assert cc1 == (0.0, 0.0)
    assert cc2 == (0.0, 0.0)
    assert cc3 == (0.0, 0.0)


def test_cc_out_of_order() -> None:
    """ Basic check with out-of-order lists """
    cc = _cross_correlation(basic_mock_gt_2,
                            basic_mock_det_2,
                            start_end_series_basic_2,
                            1)
    assert cc == (0.45, -0.2)


@patch('aqudem.cross_correlation_helper._get_timeseries_format')
def test_cc_correct_behavior_one_activity(mock_get_timeseries_format: MagicMock) -> None:
    # Note that the function inputs are not used in the function,
    # because the mock is used to control the return value
    mock_get_timeseries_format.return_value = ([-1, -1, 1, -1, -1], [-1, -1, 1, -1, -1])
    cc = _cross_correlation(basic_mock_gt,
                            basic_mock_det,
                            start_end_series_basic,
                            1)
    assert cc == (1.0, 0.0)
    mock_get_timeseries_format.return_value = ([-1, -1, 1, 1, 1], [-1, -1, 1, 1, 1])
    cc = _cross_correlation(basic_mock_gt,
                            basic_mock_det,
                            start_end_series_basic,
                            1)
    assert cc == (1.0, 0.0)
    mock_get_timeseries_format.return_value = ([-1, -1, -1, -1, -1], [-1, -1, 1, -1, -1])
    cc = _cross_correlation(basic_mock_gt,
                            basic_mock_det,
                            start_end_series_basic,
                            1)
    assert cc == (0.6, 0.0)


@patch('aqudem.cross_correlation_helper._get_timeseries_format')
def test_cc_correct_shift_behavior(mock_get_timeseries_format: MagicMock) -> None:
    # Note that the function inputs are not used in the function,
    # because the mock is used to control the return value
    mock_get_timeseries_format.return_value = ([-1, -1, 1, -1, -1], [-1, -1, -1, 1, -1])
    cc = _cross_correlation(basic_mock_gt,
                            basic_mock_det,
                            start_end_series_basic,
                            1)
    assert cc == (0.8, -0.25)


def test_context_cross_correlation() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.cross_correlation(activity_name="Activity A", case_id="ExampleTrace1")
    assert res == (0.73, 0.0)


def test_context_cross_correlation_by_activity() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.cross_correlation(activity_name="Activity A")
    assert res == (0.64, 0.225)
    res = context.cross_correlation(activity_name="Activity B")
    assert res == (0.795, 0.165)
    res = context.cross_correlation(activity_name="Activity C")
    assert res == (0.83, -0.03)


def test_context_cross_correlation_by_case() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.cross_correlation(case_id="ExampleTrace1")
    assert res == (0.8267, -0.01)
    res = context.cross_correlation(case_id="ExampleTrace2")
    assert res == (0.61, 0.39)


def test_context_cross_correlation_by_case_and_activity() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.cross_correlation()
    assert res == (0.74, 0.15)
