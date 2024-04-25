"""Test damerau levenshtein dist norm that is exposed in the context class and helper functions."""
import os
from datetime import datetime
import pytest
import static_frame as sf
import aqudem
from aqudem.damerau_levenshtein_helper import (_map_strings_to_letters,
                                               _damerau_opt_levenshtein_dist,
                                               _levenshtein_distancy_by_case,
                                               _damerau_levenshtein_distancy_by_case)


def test_basic_map_strings() -> None:
    res1, res2 = _map_strings_to_letters(["i", "think", "i", "am", "think", "think", "am", "i"],
                                         ["therefore", "therefore", "am",
                                          "i", "i", "am", "therefore", "am"])
    assert res1 == "ABACBBCA"
    assert res2 == "DDCAACDC"


def test_different_lengths_map_strings() -> None:
    res1, res2 = _map_strings_to_letters(["i", "think", "i", "am"],
                                         ["therefore", "therefore", "am", "i",
                                          "i", "am", "therefore", "am"])
    assert res1 == "ABAC"
    assert res2 == "DDCAACDC"


def test_empty_lengths_map_strings() -> None:
    res1, res2 = _map_strings_to_letters([],
                                         ["therefore", "therefore", "am", "i",
                                          "i", "am", "therefore", "am"])
    assert res1 == ""
    assert res2 == "AABCCBAB"
    res1, res2 = _map_strings_to_letters(["i", "think", "i", "am"],
                                         [])
    assert res1 == "ABAC"
    assert res2 == ""


def test_basic_damerau_opt_levenshtein_dist_norm() -> None:
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace", "ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "complete", "start", "complete"],
        "concept:name": ["A", "A", "B", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0),
                           datetime(2021, 1, 1, 0, 15, 0),
                           datetime(2021, 1, 1, 0, 20, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace", "ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "complete", "start", "complete"],
        "concept:name": ["A", "A", "B", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0),
                           datetime(2021, 1, 1, 0, 15, 0),
                           datetime(2021, 1, 1, 0, 20, 0)]
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[1] == 0.0


def test_swap_damerau_opt_levenshtein_dist_norm() -> None:
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["A", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["B", "A"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[1] == 0.5


def test_change_damerau_opt_levenshtein_dist_norm() -> None:
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["A", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["B", "A"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[1] == 0.5
    res = _damerau_opt_levenshtein_dist(gt, det, metr_type="lev")
    assert res[1] == 1.0


def test_change_damerau_opt_levenshtein_dist() -> None:
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["A", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["B", "A"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[0] == 1
    res = _damerau_opt_levenshtein_dist(gt, det, metr_type="lev")
    assert res[0] == 2


def test_change_damerau_opt_levenshtein() -> None:
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace", "ExampleTrace2",
                              "ExampleTrace2", "ExampleTrace2", "ExampleTrace2"],
        "lifecycle:transition": ["start", "start", "start", "start", "start", "start"],
        "concept:name": ["A", "B", "A", "B", "A", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0),
                           datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0),
                           datetime(2021, 1, 1, 0, 20, 0),
                           datetime(2021, 1, 1, 0, 30, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace", "ExampleTrace2",
                              "ExampleTrace2", "ExampleTrace2", "ExampleTrace2"],
        "lifecycle:transition": ["start", "start", "start", "start", "start", "start"],
        "concept:name": ["B", "A", "B", "A", "C", "C"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0),
                           datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0),
                           datetime(2021, 1, 1, 0, 20, 0),
                           datetime(2021, 1, 1, 0, 30, 0)]
    })
    res = _damerau_levenshtein_distancy_by_case(gt, det, case_id="ExampleTrace")
    assert res == (1, 0.5)
    res = _damerau_levenshtein_distancy_by_case(gt, det, case_id="ExampleTrace2")
    assert res == (3, 0.75)
    res = _damerau_levenshtein_distancy_by_case(gt, det, case_id="*")
    assert res == (2, 0.625)
    res = _levenshtein_distancy_by_case(gt, det, case_id="ExampleTrace")
    assert res == (2, 1.0)
    res = _levenshtein_distancy_by_case(gt, det, case_id="ExampleTrace2")
    assert res == (3, 0.75)
    res = _levenshtein_distancy_by_case(gt, det, case_id="*")
    assert res == (2.5, 0.875)


def test_change_all_damerau_opt_levenshtein_dist_norm() -> None:
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["A", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["C", "C"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[1] == 1.0
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["A", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": [],
        "lifecycle:transition": [],
        "concept:name": [],
        "time:timestamp": []
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[1] == 1.0


def test_empty_damerau_opt_levenshtein_dist_norm() -> None:
    gt = sf.FrameHE.from_dict({
        "case:concept:name": ["ExampleTrace", "ExampleTrace"],
        "lifecycle:transition": ["start", "start"],
        "concept:name": ["A", "B"],
        "time:timestamp": [datetime(2021, 1, 1, 0, 0, 0),
                           datetime(2021, 1, 1, 0, 10, 0)]
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": [],
        "lifecycle:transition": [],
        "concept:name": [],
        "time:timestamp": []
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[1] == 1.0
    gt = sf.FrameHE.from_dict({
        "case:concept:name": [],
        "lifecycle:transition": [],
        "concept:name": [],
        "time:timestamp": []
    })
    det = sf.FrameHE.from_dict({
        "case:concept:name": [],
        "lifecycle:transition": [],
        "concept:name": [],
        "time:timestamp": []
    })
    res = _damerau_opt_levenshtein_dist(gt, det)
    assert res[1] == 0.0


def test_context_damerau_levenshtein() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.damerau_levenshtein_distance(case_id="ExampleTrace1")
    assert res == (2, 0.3333)
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.damerau_levenshtein_distance(case_id="ExampleTrace2")
    assert res == (1, 0.3333)
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.damerau_levenshtein_distance()
    assert res == (1.5, 0.3333)


def test_context_levenshtein() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.levenshtein_distance(case_id="ExampleTrace2")
    assert res == (2, 0.6667)
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.levenshtein_distance(case_id="ExampleTrace1")
    assert res == (2, 0.3333)
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.levenshtein_distance()
    assert res == (2.0, 0.5)


def test_wrong_metr_type() -> None:
    with pytest.raises(ValueError):
        _damerau_opt_levenshtein_dist(sf.FrameHE(), sf.FrameHE(), metr_type="wrong")
