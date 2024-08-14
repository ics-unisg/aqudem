"""Tests for `aqudem` package."""
import os
import aqudem


def test_context_creation() -> None:
    """Test the creation of a context object."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    for value in context._ground_truth["concept:name"].values:
        assert value in ["Activity A", "Activity B", "Activity C"]
    for value in context._detected["concept:name"].values:
        assert value in ["Activity A", "Activity B", "Activity C"]
    for value in context._detected["case:sampling_freq"].values:
        assert value == 1.0
    assert context._ground_truth["case:concept:name"].count(unique=True) == 2
    assert context._detected["case:concept:name"].count(unique=True) == 2
    assert len(context._ground_truth.loc[
                   context._ground_truth["lifecycle:transition"] == "complete"]) == 9
    assert len(context._ground_truth.loc[
                   context._ground_truth["lifecycle:transition"] == "start"]) == 9
    assert len(context._detected.loc[
                   context._detected["lifecycle:transition"] == "complete"]) == 8
    assert len(context._detected.loc[
                   context._detected["lifecycle:transition"] == "start"]) == 8


def test_context_creation_multiple_traces() -> None:
    """Test the creation of a context object."""
    aqudem.Context(os.path.join("tests", "resources", "ground_truth_multipletraces.xes"),
                   os.path.join("tests", "resources", "detected_multipletraces.xes"))


def test_get_activity_names() -> None:
    """Test the get_activity_names method."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    act_names = context.activity_names
    assert "Activity A" in act_names["ground_truth"]
    assert "Activity B" in act_names["ground_truth"]
    assert "Activity C" in act_names["ground_truth"]
    assert "Activity A" in act_names["detected"]
    assert "Activity B" in act_names["detected"]
    assert "Activity C" in act_names["detected"]
    assert len(act_names["ground_truth"]) == 3
    assert len(act_names["detected"]) == 3


def test_get_case_ids() -> None:
    """Test the get_case_ids method."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth_multipletraces.xes"),
                             os.path.join("tests", "resources", "detected_multipletraces.xes"))
    case_ids = context.case_ids
    assert isinstance(case_ids, dict)
    assert ["ground_truth", "detected"] == list(case_ids.keys())
    assert "ExampleTrace" in case_ids["ground_truth"]
    assert "ExampleTrace2" in case_ids["ground_truth"]
    assert "ExampleTrace" in case_ids["detected"]
    assert "ExampleTrace2" in case_ids["detected"]
    assert len(case_ids["ground_truth"]) == 2
    assert len(case_ids["detected"]) == 2
