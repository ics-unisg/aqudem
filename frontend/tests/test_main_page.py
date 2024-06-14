"""Tests the interactive tab after the file upload."""
import os
import pytest
from streamlit.testing.v1 import AppTest
import aqudem

CASE_METRICS = ["Damerau-Levenshtein", "Levenshtein",
                "Damerau-Levenshtein normalized", "Levenshtein normalized"]
CASE_ACTIVITY_METRICS = ["Cross-correlation", "2SET metrics", "2SET rates",
                         "Event analysis", "Event analysis rates"]


@pytest.fixture(scope="module", name='at')
def fixture_app_test() -> AppTest:
    gt_path = os.path.join("tests", "resources", "gt.xes")
    detected_path = os.path.join("tests", "resources", "det.xes")
    mock_cont = aqudem.Context(gt_path, detected_path)
    at = AppTest.from_file("aqudem_app.py")
    at.session_state.active_analysis = True
    at.session_state.context = mock_cont
    at.run(timeout=10)

    assert not at.exception
    return at


def test_all_metrics_have_case_choice(at: AppTest) -> None:
    assert at.selectbox[0].label == "Which metric are you interested in?"
    for metric in CASE_METRICS + CASE_ACTIVITY_METRICS:
        assert at.selectbox[0].label == "Which metric are you interested in?"
        at.selectbox[0].select(metric).run(timeout=10)
        labels = []
        for i in range(at.multiselect.len):
            labels.append(at.multiselect[i].label)
        assert any("Which cases are you interested in?"
                   == lab for lab in labels)


def test_some_metrics_have_activity_choice(at: AppTest) -> None:
    assert at.selectbox[0].label == "Which metric are you interested in?"
    for metric in CASE_ACTIVITY_METRICS:
        assert at.selectbox[0].label == "Which metric are you interested in?"
        at.selectbox[0].select(metric).run(timeout=10)
        labels = []
        for i in range(at.multiselect.len):
            labels.append(at.multiselect[i].label)
        assert any("Which activities are you interested in?"
                   == lab for lab in labels)


def test_all_metrics_have_suitable_dataframes(at: AppTest) -> None:
    assert at.tabs[0].dataframe.len == 1
    for metric in CASE_METRICS + CASE_ACTIVITY_METRICS:
        at.selectbox[0].select(metric).run(timeout=10)
        assert "case" in at.tabs[0].dataframe[0].value.columns
    for metric in CASE_ACTIVITY_METRICS:
        at.selectbox[0].select(metric).run(timeout=10)
        assert "activity" in at.tabs[0].dataframe[0].value.columns


def test_tags_selection_dataframe_exists(at: AppTest) -> None:
    assert at.tabs[1].dataframe.len == 1
    assert "Tag Name" in at.tabs[1].dataframe[0].value.columns
    assert "Tag Value" in at.tabs[1].dataframe[0].value.columns
