"""Tests for the event_analysis_helper module."""
import os
import aqudem
from aqudem.event_analysis_helper import (_event_analysis, EventAnalysis,
                                          _event_analysis_by_activity_case)
from .mocks.logs import (ground_truth_ten_eighteen, detected_ten_eighteen,
                         ground_truth_ten_eleven, detected_ten_eleven,
                         ground_truth_mixed_activity, detected_mixed_activity,
                         ground_truth_mixed_case, detected_mixed_case,
                         start_end_series_ten_eleven, start_end_series_ten_eighteen,
                         start_end_series_mixed_activity, start_end_series_mixed_case)


def _verify_ten_eleven_metrics(result: EventAnalysis) -> None:
    """ Verify the metrics for the 10-11 logs."""
    assert isinstance(result, EventAnalysis)
    assert result.d == 0
    assert result.f == 1
    assert result.fm == 0
    assert result.m == 0
    assert result.c == 4
    assert result.md == 0
    assert result.fmd == 0
    assert result.fd == 2
    assert result.id == 1
    assert result.total_gt_events == 3
    assert result.total_det_events == 5


def _verify_ten_eleven_rates(result: EventAnalysis) -> None:
    """ Verify the rates for the 10-11 logs."""
    assert isinstance(result, EventAnalysis)
    assert result.dr == 0.0
    assert result.fr == 0.3333
    assert result.fmr == 0.0
    assert result.mr == 0.0
    assert result.cr_gt == 0.6667
    assert result.mdr == 0.0
    assert result.fdr == 0.4
    assert result.idr == 0.2
    assert result.cr_det == 0.4


def _verify_ten_eighteen_metrics(result: EventAnalysis) -> None:
    """ Verify the metrics for the 10-18 logs."""
    assert isinstance(result, EventAnalysis)
    assert result.d == 0
    assert result.f == 2
    assert result.fm == 0
    assert result.m == 0
    assert result.c == 2
    assert result.md == 0
    assert result.fmd == 0
    assert result.fd == 4
    assert result.id == 0
    assert result.total_gt_events == 3
    assert result.total_det_events == 5


def _verify_ten_eighteen_rates(result: EventAnalysis) -> None:
    """ Verify the rates for the 10-18 logs."""
    assert isinstance(result, EventAnalysis)
    assert result.dr == 0.0
    assert result.fr == 0.6667
    assert result.fmr == 0.0
    assert result.mr == 0.0
    assert result.cr_gt == 0.3333
    assert result.mdr == 0.0
    assert result.fdr == 0.8
    assert result.idr == 0.0
    assert result.cr_det == 0.2


def test_event_analysis_ten_eleven() -> None:
    """ Test the event analysis for the 10-11 logs."""
    result = _event_analysis(ground_truth_ten_eleven,
                             detected_ten_eleven,
                             start_end_series_ten_eleven)
    _verify_ten_eleven_metrics(result)


def test_event_analysis_rates_ten_eleven() -> None:
    """ Test the event analysis rates for the 10-11 logs."""
    result = _event_analysis(ground_truth_ten_eleven,
                             detected_ten_eleven,
                             start_end_series_ten_eleven)
    _verify_ten_eleven_rates(result)


def test_event_analysis_ten_eighteen() -> None:
    result = _event_analysis(ground_truth_ten_eighteen,
                             detected_ten_eighteen,
                             start_end_series_ten_eighteen)
    _verify_ten_eighteen_metrics(result)


def test_event_analysis_rates_ten_eighteen() -> None:
    result = _event_analysis(ground_truth_ten_eighteen,
                             detected_ten_eighteen,
                             start_end_series_ten_eighteen)
    _verify_ten_eighteen_rates(result)


def test_event_analysis_by_activity() -> None:
    result = _event_analysis_by_activity_case(ground_truth_mixed_activity,
                                              detected_mixed_activity,
                                              "A",
                                              "1",
                                              start_end_series_mixed_activity)
    _verify_ten_eleven_metrics(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_activity,
                                              detected_mixed_activity,
                                              "B",
                                              "1",
                                              start_end_series_mixed_activity)
    _verify_ten_eighteen_metrics(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_activity,
                                              detected_mixed_activity,
                                              "*",
                                              "1",
                                              start_end_series_mixed_activity)
    assert isinstance(result, EventAnalysis)
    assert result.d == 0
    assert result.f == 1.5
    assert result.fm == 0
    assert result.m == 0
    assert result.c == 3
    assert result.md == 0
    assert result.fmd == 0
    assert result.fd == 3
    assert result.id == 0.5
    assert result.total_gt_events == 3
    assert result.total_det_events == 5


def test_event_analysis_rates_by_activity() -> None:
    result = _event_analysis_by_activity_case(ground_truth_mixed_activity,
                                              detected_mixed_activity,
                                              "A",
                                              "1",
                                              start_end_series_mixed_activity)
    _verify_ten_eleven_rates(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_activity,
                                              detected_mixed_activity,
                                              "B",
                                              "1",
                                              start_end_series_mixed_activity)
    _verify_ten_eighteen_rates(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_activity,
                                              detected_mixed_activity,
                                              "*",
                                              "1",
                                              start_end_series_mixed_activity)
    assert isinstance(result, EventAnalysis)
    assert result.dr == 0.0
    assert result.fr == 0.5
    assert result.fmr == 0.0
    assert result.mr == 0.0
    assert result.cr_gt == 0.5
    assert result.mdr == 0.0
    assert result.fdr == 0.6
    assert result.idr == 0.1
    assert result.cr_det == 0.3


def test_event_analysis_by_activity_case() -> None:
    result = _event_analysis_by_activity_case(ground_truth_mixed_case,
                                              detected_mixed_case,
                                              "*",
                                              "1",
                                              start_end_series_mixed_case)
    _verify_ten_eleven_metrics(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_case,
                                              detected_mixed_case,
                                              "*",
                                              "2",
                                              start_end_series_mixed_case)
    _verify_ten_eighteen_metrics(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_case,
                                              detected_mixed_case,
                                              "*",
                                              "*",
                                              start_end_series_mixed_case)
    assert isinstance(result, EventAnalysis)
    assert result.d == 0
    assert result.f == 1.5
    assert result.fm == 0
    assert result.m == 0
    assert result.c == 3
    assert result.md == 0
    assert result.fmd == 0
    assert result.fd == 3
    assert result.id == 0.5
    assert result.total_gt_events == 3
    assert result.total_det_events == 5


def test_event_analysis_rates_by_activity_case() -> None:
    result = _event_analysis_by_activity_case(ground_truth_mixed_case,
                                              detected_mixed_case,
                                              "*",
                                              "1",
                                              start_end_series_mixed_case)
    _verify_ten_eleven_rates(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_case,
                                              detected_mixed_case,
                                              "*",
                                              "2",
                                              start_end_series_mixed_case)
    _verify_ten_eighteen_rates(result)
    result = _event_analysis_by_activity_case(ground_truth_mixed_case,
                                              detected_mixed_case,
                                              "*",
                                              "*",
                                              start_end_series_mixed_case)
    assert isinstance(result, EventAnalysis)
    assert result.dr == 0.0
    assert result.fr == 0.5
    assert result.fmr == 0.0
    assert result.mr == 0.0
    assert result.cr_gt == 0.5
    assert result.mdr == 0.0
    assert result.fdr == 0.6
    assert result.idr == 0.1
    assert result.cr_det == 0.3


def test_context_ea_1_a() -> None:
    """Test EA metrics that are exposed in the context class for trace 1, activity A."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity A", case_id="ExampleTrace1")
    assert isinstance(res, EventAnalysis)
    assert res.d == 0
    assert res.f == 1
    assert res.fm == 0
    assert res.m == 0
    assert res.c == 2
    assert res.md == 0
    assert res.fmd == 0
    assert res.fd == 2
    assert res.id == 0


def test_context_ea_1_b() -> None:
    """Test EA metrics that are exposed in the context class for trace 1, activity B."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity B", case_id="ExampleTrace1")
    assert isinstance(res, EventAnalysis)
    assert res.d == 0
    assert res.f == 0
    assert res.fm == 0
    assert res.m == 2
    assert res.c == 0
    assert res.md == 1
    assert res.fmd == 0
    assert res.fd == 0
    assert res.id == 0


def test_context_ea_1_c() -> None:
    """Test EA metrics that are exposed in the context class for trace 1, activity C."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity C", case_id="ExampleTrace1")
    assert isinstance(res, EventAnalysis)
    assert res.d == 1
    assert res.f == 0
    assert res.fm == 0
    assert res.m == 0
    assert res.c == 2
    assert res.md == 0
    assert res.fmd == 0
    assert res.fd == 0
    assert res.id == 0


def test_context_ea_2_a() -> None:
    """Test EA metrics that are exposed in the context class for trace 2, activity A."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity A", case_id="ExampleTrace2")
    assert isinstance(res, EventAnalysis)
    assert res.d == 1
    assert res.f == 0
    assert res.fm == 0
    assert res.m == 0
    assert res.c == 0
    assert res.md == 0
    assert res.fmd == 0
    assert res.fd == 0
    assert res.id == 1


def test_context_ea_2_b() -> None:
    """Test EA metrics that are exposed in the context class for trace 2, activity B."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity B", case_id="ExampleTrace2")
    assert isinstance(res, EventAnalysis)
    assert res.d == 0
    assert res.f == 0
    assert res.fm == 1
    assert res.m == 1
    assert res.c == 0
    assert res.md == 0
    assert res.fmd == 1
    assert res.fd == 1
    assert res.id == 0


def test_context_ea_rates_1_a() -> None:
    """Test EA rates that are exposed in the context class for trace 1, activity A."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity A", case_id="ExampleTrace1")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0.0
    assert res.fr == 0.5
    assert res.fmr == 0.0
    assert res.mr == 0.0
    assert res.cr_gt == 0.5
    assert res.cr_det == round(1 / 3, 4)
    assert res.mdr == 0.0
    assert res.fmdr == 0.0
    assert res.fdr == round(2 / 3, 4)
    assert res.idr == 0.0


def test_context_ea_rates_1_b() -> None:
    """Test EA rates that are exposed in the context class for trace 1, activity B."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity B", case_id="ExampleTrace1")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0.0
    assert res.fr == 0.0
    assert res.fmr == 0.0
    assert res.mr == 1.0
    assert res.cr_gt == 0.0
    assert res.cr_det == 0.0
    assert res.mdr == 1.0
    assert res.fmdr == 0.0
    assert res.fdr == 0.0
    assert res.idr == 0.0


def test_context_ea_rates_1_c() -> None:
    """Test EA rates that are exposed in the context class for trace 1, activity C."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity C", case_id="ExampleTrace1")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0.5
    assert res.fr == 0.0
    assert res.fmr == 0.0
    assert res.mr == 0.0
    assert res.cr_gt == 0.5
    assert res.cr_det == 1.0
    assert res.mdr == 0.0
    assert res.fmdr == 0.0
    assert res.fdr == 0.0
    assert res.idr == 0.0


def test_context_ea_rates_2_a() -> None:
    """Test EA rates that are exposed in the context class for trace 2, activity A."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity A", case_id="ExampleTrace2")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 1.0
    assert res.fr == 0.0
    assert res.fmr == 0.0
    assert res.mr == 0.0
    assert res.cr_gt == 0.0
    assert res.cr_det == 0.0
    assert res.mdr == 0.0
    assert res.fmdr == 0.0
    assert res.fdr == 0.0
    assert res.idr == 1.0


def test_context_ea_rates_2_b() -> None:
    """Test EA rates that are exposed in the context class for trace 2, activity B."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity B", case_id="ExampleTrace2")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0.0
    assert res.fr == 0.0
    assert res.fmr == 0.5
    assert res.mr == 0.5
    assert res.cr_gt == 0.0
    assert res.cr_det == 0.0
    assert res.mdr == 0.0
    assert res.fmdr == 0.5
    assert res.fdr == 0.5
    assert res.idr == 0.0


def test_context_ea_by_activity() -> None:
    """Test EA by activity that is exposed in the context class."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity A")
    assert isinstance(res, EventAnalysis)
    assert res.d == round((0 + 1) / 2, 4)
    assert res.f == round((1 + 0) / 2, 4)
    assert res.fm == round((0 + 0) / 2, 4)
    assert res.m == round((0 + 0) / 2, 4)
    assert res.c == round((2 + 0) / 2, 4)
    assert res.md == round((0 + 0) / 2, 4)
    assert res.fmd == round((0 + 0) / 2, 4)
    assert res.fd == round((2 + 0) / 2, 4)
    assert res.id == round((0 + 1) / 2, 4)
    assert res.total_gt_events == 1.5
    assert res.total_det_events == 2
    res = context.event_analysis(activity_name="Activity B")
    assert isinstance(res, EventAnalysis)
    assert res.d == round((0 + 0) / 2, 4)
    assert res.f == round((0 + 0) / 2, 4)
    assert res.fm == round((0 + 1) / 2, 4)
    assert res.m == round((2 + 1) / 2, 4)
    assert res.c == round((0 + 0) / 2, 4)
    assert res.md == round((0 + 1) / 2, 4)
    assert res.fmd == round((0 + 1) / 2, 4)
    assert res.fd == round((0 + 1) / 2, 4)
    assert res.id == round((0 + 0) / 2, 4)
    assert res.total_gt_events == 2
    assert res.total_det_events == 1.5
    res = context.event_analysis(activity_name="Activity C")
    assert isinstance(res, EventAnalysis)
    assert res.d == 1
    assert res.f == 0
    assert res.fm == 0
    assert res.m == 0
    assert res.c == 2
    assert res.md == 0
    assert res.fmd == 0
    assert res.fd == 0
    assert res.id == 0
    assert res.total_gt_events == 2
    assert res.total_det_events == 1


def test_context_ea_by_activity_case() -> None:
    """Test EA by activity and case that is exposed in the context class."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis()
    assert isinstance(res, EventAnalysis)
    assert res.d == round((0 + 0 + 1 + 1 + 0) / 5, 4)
    assert res.f == round((1 + 0 + 0 + 0 + 0) / 5, 4)
    assert res.fm == round((0 + 0 + 0 + 0 + 1) / 5, 4)
    assert res.m == round((0 + 2 + 0 + 0 + 1) / 5, 4)
    assert res.c == round((2 + 0 + 2 + 0 + 0) / 5, 4)
    assert res.md == round((0 + 1 + 0 + 0 + 0) / 5, 4)
    assert res.fmd == round((0 + 0 + 0 + 0 + 1) / 5, 4)
    assert res.fd == round((2 + 0 + 0 + 0 + 1) / 5, 4)
    assert res.id == round((0 + 0 + 0 + 0 + 1) / 5, 4)
    assert res.total_gt_events == 1.8
    assert res.total_det_events == 1.6


def test_context_ea_rates_by_activity() -> None:
    """Test EA rates by activity that is exposed in the context class, aggregated by activity."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis(activity_name="Activity A")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0.3333
    assert res.fr == 0.3333
    assert res.fmr == 0
    assert res.mr == 0
    assert res.cr_gt == 0.3333
    assert res.cr_det == 0.25
    assert res.mdr == 0
    assert res.fmdr == 0
    assert res.fdr == 0.5
    assert res.idr == 0.25
    res = context.event_analysis(activity_name="Activity B")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0
    assert res.fr == 0
    assert res.fmr == 0.25
    assert res.mr == 0.75
    assert res.cr_gt == 0
    assert res.cr_det == 0
    assert res.mdr == 0.3333
    assert res.fmdr == 0.3333
    assert res.fdr == 0.3333
    assert res.idr == 0
    res = context.event_analysis(activity_name="Activity C")
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0.5
    assert res.fr == 0.0
    assert res.fmr == 0.0
    assert res.mr == 0.0
    assert res.cr_gt == 0.5
    assert res.cr_det == 1.0
    assert res.mdr == 0.0
    assert res.fmdr == 0.0
    assert res.fdr == 0.0
    assert res.idr == 0.0


def test_context_ea_rates_by_activity_case() -> None:
    """Test EA rates by activity and case that is exposed in the context class,
    aggregated by activity and case."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis()
    assert isinstance(res, EventAnalysis)
    assert res.dr == 0.2222
    assert res.fr == 0.1111
    assert res.fmr == 0.1111
    assert res.mr == 0.3333
    assert res.cr_gt == 0.2222
    assert res.cr_det == 0.25
    assert res.mdr == 0.125
    assert res.fmdr == 0.125
    assert res.fdr == 0.375
    assert res.idr == 0.125


def test_ea_recall_precision_f1() -> None:
    """Test EA rates by activity and case that is exposed in the context class,
    aggregated by activity and case."""
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.event_analysis()
    assert isinstance(res, EventAnalysis)
    assert 0 <= res.recall <= 1
    assert 0 <= res.precision <= 1
    assert 0 <= res.f1 <= 1
