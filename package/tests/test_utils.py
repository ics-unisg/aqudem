"""This module contains tests for the aqudem utils module."""
import os
import pytest
import aqudem


def test_xes_check_missing_sampling_freq() -> None:
    """Test the XESMissingSamplingFreqError exception."""
    with pytest.raises(aqudem.utils.XESSamplingFreqError):
        aqudem.Context(os.path.join("tests", "resources", "ground_truth_missingsamplingfreq.xes"),
                       os.path.join("tests", "resources", "detected_missingsamplingfreq.xes"))


def test_xes_missing_lifecycle_transition() -> None:
    """Test the XESIncorrectLifecycleTransitionError exception."""
    with pytest.raises(aqudem.utils.XESIncorrectLifecycleTransitionError):
        aqudem.Context(os.path.join("tests", "resources", "ground_truth_missinglifecycle.xes"),
                       os.path.join("tests", "resources", "detected_missinglifecycle.xes"))


def test_xes_wrong_lifecycle_transition() -> None:
    """Test the XESIncorrectLifecycleTransitionError exception."""
    with pytest.raises(aqudem.utils.XESIncorrectLifecycleTransitionError):
        aqudem.Context(os.path.join("tests", "resources", "ground_truth_wronglifecycle.xes"),
                       os.path.join("tests", "resources", "detected_wronglifecycle.xes"))


def test_xes_toomanycomplete_lifecycle_transition() -> None:
    """Test the XESIncorrectLifecycleTransitionError exception."""
    with pytest.raises(aqudem.utils.XESIncorrectLifecycleTransitionError):
        aqudem.Context(os.path.join("tests",
                                    "resources",
                                    "ground_truth_toomanycompletelifecycle.xes"),
                       os.path.join("tests", "resources", "detected_toomanycompletelifecycle.xes"))


def test_xes_missing_timestamp() -> None:
    """Test the XESMissingTimestamp exception."""
    with pytest.raises(aqudem.utils.XESMissingTimestamp):
        aqudem.Context(os.path.join("tests", "resources", "ground_truth_missingtimestamp.xes"),
                       os.path.join("tests", "resources", "detected_missingtimestamp.xes"))


def test_xes_missing_activity_name() -> None:
    """Test the XESMissingActivityName exception."""
    with pytest.raises(aqudem.utils.XESMissingActivityName):
        aqudem.Context(os.path.join("tests", "resources", "ground_truth_missingactivityname.xes"),
                       os.path.join("tests", "resources", "detected_missingactivityname.xes"))


def test_xes_missing_trace_name() -> None:
    """Test the XESMissingTraceNameAttribute exception."""
    with pytest.raises(aqudem.utils.XESMissingTraceNameAttribute):
        aqudem.Context(os.path.join("tests", "resources", "ground_truth_missingtracename.xes"),
                       os.path.join("tests", "resources", "detected_missingtracename.xes"))


def test_initialization_error_case_missing() -> None:
    """Test the initialization of the context object with case mismatch/missing case."""
    with pytest.raises(ValueError) as e:
        aqudem.Context(os.path.join("tests", "resources", "ground_truth_no_matching_case.xes"),
                       os.path.join("tests", "resources", "detected_no_matching_case.xes"))
    assert "Currently, all case IDs must be in both logs." in str(e.value)


def test_initialization_inconsistent_samping_freq() -> None:
    """Test the initialization of the context object with inconsistent sampling frequency."""
    with pytest.raises(aqudem.utils.XESSamplingFreqError):
        aqudem.Context(
            os.path.join("tests", "resources", "ground_truth_inconsistent_sampling_freq.xes"),
            os.path.join("tests", "resources", "detected_inconsistent_sampling_freq.xes"))
