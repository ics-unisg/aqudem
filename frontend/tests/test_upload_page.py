"""Tests for the first page after starting the app,
where the user can upload the files."""
import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture(scope="module", name='at')
def fixture_app_test() -> AppTest:
    at = AppTest.from_file("aqudem_app.py")
    at.run()
    assert not at.exception
    return at


def test_start_analysis_button_exists(at: AppTest) -> None:
    assert at.button.len == 1
    assert at.button[0].label == "Start analysis"


def test_correct_text_elements_exist(at: AppTest) -> None:
    assert at.header.len == 1
    assert "AquDeM" in at.header[0].value
    assert any("upload the ground truth and detected logs"
               in md_text for md_text
               in at.markdown.values)


def test_starting_analysis_without_files_leads_to_warning(at:AppTest) -> None:
    assert at.toast.len == 0
    at.button[0].click().run()
    assert at.toast.len == 1
    assert "Please upload" in at.toast[0].value
