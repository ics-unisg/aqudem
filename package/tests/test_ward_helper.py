"""This module contains tests for the aqudem utils module."""
from datetime import datetime
import numpy as np
import static_frame as sf
import pytest
from aqudem import ward_helper
from aqudem.ward_helper import _is_during_activity_exec
from .mocks.logs import detected_ten_eleven, ground_truth_ten_eleven, start_end_series_ten_eleven


def test_generate_eight_type_with_valid_input() -> None:
    assert ward_helper._generate_eight_type("TP", "FP", "TN") == "Oo"


def test_generate_eight_type_with_invalid_segment_type() -> None:
    with pytest.raises(ValueError):
        ward_helper._generate_eight_type("Invalid", "FP", "TN")


def test_generate_eight_type_with_invalid_curr_type() -> None:
    with pytest.raises(ValueError):
        ward_helper._generate_eight_type("TP", "Invalid", "TN")


def test_generate_eight_type_with_invalid_prev_type() -> None:
    with pytest.raises(ValueError):
        ward_helper._generate_eight_type("NaN", "FP", "TN")


def test_generate_eight_type_with_invalid_next_type() -> None:
    with pytest.raises(ValueError):
        ward_helper._generate_eight_type("TP", "FP", "Invalid")


def test_generate_segment_scores_with_valid_input() -> None:
    ground_truth = sf.FrameHE.from_dict({
        "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete"],
        "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 12, 0),
                           datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 15, 0),
                           datetime(2021, 1, 1, 16, 0), datetime(2021, 1, 1, 18, 0)]
    }, dtypes={"lifecycle:transition": str, "time:timestamp": np.datetime64})
    detected = sf.FrameHE.from_dict({
        "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete",
                                 "start", "complete", "start", "complete"],
        "time:timestamp": [datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 11, 0),
                           datetime(2021, 1, 1, 11, 30), datetime(2021, 1, 1, 12, 30),
                           datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 14, 0),
                           datetime(2021, 1, 1, 14, 30), datetime(2021, 1, 1, 15, 30),
                           datetime(2021, 1, 1, 15, 45), datetime(2021, 1, 1, 17, 0)]
    }, dtypes={"lifecycle:transition": str, "time:timestamp": np.datetime64})
    result = ward_helper._generate_segment_scores(ground_truth,
                                                  detected,
                                                  datetime(2021, 1, 1, 10, 0),
                                                  datetime(2021, 1, 1, 18, 0))
    assert len(result) != 0
    assert "start" in result.columns
    assert "end" in result.columns
    assert "type" in result.columns

    assert result.iloc[0]["type"] == "Ua"
    assert result.iloc[0]["start"] == datetime(2021, 1, 1, 10, 0)
    assert result.iloc[0]["end"] == datetime(2021, 1, 1, 10, 15)

    assert result.iloc[1]["type"] == "TP"
    assert result.iloc[1]["start"] == datetime(2021, 1, 1, 10, 15)
    assert result.iloc[1]["end"] == datetime(2021, 1, 1, 11, 0)

    assert result.iloc[2]["type"] == "F"
    assert result.iloc[2]["start"] == datetime(2021, 1, 1, 11, 0)
    assert result.iloc[2]["end"] == datetime(2021, 1, 1, 11, 30)

    assert result.iloc[3]["type"] == "TP"
    assert result.iloc[3]["start"] == datetime(2021, 1, 1, 11, 30)
    assert result.iloc[3]["end"] == datetime(2021, 1, 1, 12, 0)

    assert result.iloc[4]["type"] == "Oo"
    assert result.iloc[4]["start"] == datetime(2021, 1, 1, 12, 0)
    assert result.iloc[4]["end"] == datetime(2021, 1, 1, 12, 30)

    assert result.iloc[5]["type"] == "TN"
    assert result.iloc[5]["start"] == datetime(2021, 1, 1, 12, 30)
    assert result.iloc[5]["end"] == datetime(2021, 1, 1, 13, 0)

    assert result.iloc[6]["type"] == "TP"
    assert result.iloc[6]["start"] == datetime(2021, 1, 1, 13, 0)
    assert result.iloc[6]["end"] == datetime(2021, 1, 1, 14, 0)

    assert result.iloc[7]["type"] == "F"
    assert result.iloc[7]["start"] == datetime(2021, 1, 1, 14, 0)
    assert result.iloc[7]["end"] == datetime(2021, 1, 1, 14, 30)

    assert result.iloc[8]["type"] == "TP"
    assert result.iloc[8]["start"] == datetime(2021, 1, 1, 14, 30)
    assert result.iloc[8]["end"] == datetime(2021, 1, 1, 15, 0)

    assert result.iloc[9]["type"] == "Oo"
    assert result.iloc[9]["start"] == datetime(2021, 1, 1, 15, 0)
    assert result.iloc[9]["end"] == datetime(2021, 1, 1, 15, 30)

    assert result.iloc[10]["type"] == "TN"
    assert result.iloc[10]["start"] == datetime(2021, 1, 1, 15, 30)
    assert result.iloc[10]["end"] == datetime(2021, 1, 1, 15, 45)

    assert result.iloc[11]["type"] == "Oa"
    assert result.iloc[11]["start"] == datetime(2021, 1, 1, 15, 45)
    assert result.iloc[11]["end"] == datetime(2021, 1, 1, 16, 0)

    assert result.iloc[12]["type"] == "TP"
    assert result.iloc[12]["start"] == datetime(2021, 1, 1, 16, 0)
    assert result.iloc[12]["end"] == datetime(2021, 1, 1, 17, 0)

    assert result.iloc[13]["type"] == "Uo"
    assert result.iloc[13]["start"] == datetime(2021, 1, 1, 17, 0)
    assert result.iloc[13]["end"] == datetime(2021, 1, 1, 18, 0)


# pylint: disable=too-many-statements, unsubscriptable-object
def test_generate_segment_scores_with_valid_input_2() -> None:
    result = ward_helper._generate_segment_scores(ground_truth_ten_eleven,
                                                  detected_ten_eleven,
                                                  start_end_series_ten_eleven["1"][0],
                                                  start_end_series_ten_eleven["1"][1])
    assert len(result) != 0
    assert "start" in result.columns
    assert "end" in result.columns
    assert "type" in result.columns

    assert result.iloc[0]["type"] == "Oa"
    assert result.iloc[0]["start"] == datetime(2021, 1, 1, 10, 0)
    assert result.iloc[0]["end"] == datetime(2021, 1, 1, 10, 5)

    assert result.iloc[1]["type"] == "TP"
    assert result.iloc[1]["start"] == datetime(2021, 1, 1, 10, 5)
    assert result.iloc[1]["end"] == datetime(2021, 1, 1, 10, 10)

    assert result.iloc[2]["type"] == "F"
    assert result.iloc[2]["start"] == datetime(2021, 1, 1, 10, 10)
    assert result.iloc[2]["end"] == datetime(2021, 1, 1, 10, 15)

    assert result.iloc[3]["type"] == "TP"
    assert result.iloc[3]["start"] == datetime(2021, 1, 1, 10, 15)
    assert result.iloc[3]["end"] == datetime(2021, 1, 1, 10, 20)

    assert result.iloc[4]["type"] == "Uo"
    assert result.iloc[4]["start"] == datetime(2021, 1, 1, 10, 20)
    assert result.iloc[4]["end"] == datetime(2021, 1, 1, 10, 25)

    assert result.iloc[5]["type"] == "TN"
    assert result.iloc[5]["start"] == datetime(2021, 1, 1, 10, 25)
    assert result.iloc[5]["end"] == datetime(2021, 1, 1, 10, 30)

    assert result.iloc[6]["type"] == "Oa"
    assert result.iloc[6]["start"] == datetime(2021, 1, 1, 10, 30)
    assert result.iloc[6]["end"] == datetime(2021, 1, 1, 10, 35)

    assert result.iloc[7]["type"] == "TP"
    assert result.iloc[7]["start"] == datetime(2021, 1, 1, 10, 35)
    assert result.iloc[7]["end"] == datetime(2021, 1, 1, 10, 38)

    assert result.iloc[8]["type"] == "Oo"
    assert result.iloc[8]["start"] == datetime(2021, 1, 1, 10, 38)
    assert result.iloc[8]["end"] == datetime(2021, 1, 1, 10, 40)

    assert result.iloc[9]["type"] == "TN"
    assert result.iloc[9]["start"] == datetime(2021, 1, 1, 10, 40)
    assert result.iloc[9]["end"] == datetime(2021, 1, 1, 10, 41)

    assert result.iloc[10]["type"] == "I"
    assert result.iloc[10]["start"] == datetime(2021, 1, 1, 10, 41)
    assert result.iloc[10]["end"] == datetime(2021, 1, 1, 10, 42)

    assert result.iloc[11]["type"] == "TN"
    assert result.iloc[11]["start"] == datetime(2021, 1, 1, 10, 42)
    assert result.iloc[11]["end"] == datetime(2021, 1, 1, 10, 45)

    assert result.iloc[12]["type"] == "Ua"
    assert result.iloc[12]["start"] == datetime(2021, 1, 1, 10, 45)
    assert result.iloc[12]["end"] == datetime(2021, 1, 1, 10, 50)

    assert result.iloc[13]["type"] == "TP"
    assert result.iloc[13]["start"] == datetime(2021, 1, 1, 10, 50)
    assert result.iloc[13]["end"] == datetime(2021, 1, 1, 10, 55)

    assert result.iloc[14]["type"] == "Oo"
    assert result.iloc[14]["start"] == datetime(2021, 1, 1, 10, 55)
    assert result.iloc[14]["end"] == datetime(2021, 1, 1, 11, 0)


def test_generate_segment_scores_with_empty_input() -> None:
    ground_truth = sf.FrameHE.from_dict({
        "lifecycle:transition": [],
        "time:timestamp": []
    })
    detected = sf.FrameHE.from_dict({
        "lifecycle:transition": [],
        "time:timestamp": []
    })
    result = ward_helper._generate_segment_scores(ground_truth, detected, None, None)
    assert len(result) == 0


def test_is_during_activity_exec() -> None:
    # Test case where timestamp is during an activity execution
    log = sf.FrameHE.from_dict({
        "lifecycle:transition": ["start", "complete"],
        "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 11, 0)]
    })
    timestamp = datetime(2021, 1, 1, 10, 30)
    assert _is_during_activity_exec(log, timestamp) is True

    # Test case where timestamp is not during an activity execution
    log = sf.FrameHE.from_dict({
        "lifecycle:transition": ["start", "complete"],
        "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 11, 0)]
    })
    timestamp = datetime(2021, 1, 1, 11, 30)
    assert _is_during_activity_exec(log, timestamp) is False

    # Test case where timestamp is exactly at the start of an activity
    log = sf.FrameHE.from_dict({
        "lifecycle:transition": ["start", "complete"],
        "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 11, 0)]
    })
    timestamp = datetime(2021, 1, 1, 10, 0)
    assert _is_during_activity_exec(log, timestamp) is True

    # Test case where timestamp is exactly at the end of an activity
    log = sf.FrameHE.from_dict({
        "lifecycle:transition": ["start", "complete"],
        "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 11, 0)]
    })
    timestamp = datetime(2021, 1, 1, 11, 0)
    assert _is_during_activity_exec(log, timestamp) is False

    # Test case where log is empty
    log = sf.FrameHE.from_dict({
        "lifecycle:transition": [],
        "time:timestamp": []
    })
    timestamp = datetime(2021, 1, 1, 10, 0)
    assert _is_during_activity_exec(log, timestamp) is False

    # Test case where lifecycle:transition is not in ["start", "complete"]
    log = sf.FrameHE.from_dict({
        "lifecycle:transition": ["other"],
        "time:timestamp": [datetime(2021, 1, 1, 10, 0)]
    })
    timestamp = datetime(2021, 1, 1, 10, 0)
    with pytest.raises(ValueError):
        _is_during_activity_exec(log, timestamp)
