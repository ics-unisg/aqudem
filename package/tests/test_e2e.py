""" Testing the aqudem package end-to-end. """
import os
from collections import Counter
from typing import Set

import pytest
import static_frame as sf
import aqudem

ACTIVIES_GT_03_20 = ['OV Burn', 'Sorting Machine sort', 'WT Transport', 'Calibrate VGR',
               'Get Workpiece from Pickup Station', 'Pickup and transport to sink',
               'Pickup and transport to Oven', 'Unload from HBW', 'Store Workpiece in HBW',
               'Calibrate HBW', 'Start Milling Machine', 'Move to DPS']
ACTIVITIES_DET_03_20 = ['WT Transport', 'Get Workpiece from Pickup Station',
                  'Store Workpiece in HBW', 'Calibrate HBW', 'Read Color', 'Move to DPS']
CASES_GT_03_20 = ['case1']
CASES_DET_03_20 = ['case1']

def get_set_all_activities(context: aqudem.Context) -> Set[str]:
    return set(context.activity_names["ground_truth"] + context.activity_names["detected"])

def get_set_all_cases(context: aqudem.Context) -> Set[str]:
    return set(context.case_ids["ground_truth"] + context.case_ids["detected"])

def act_only_in_one_log(context: aqudem.Context) -> Set[str]:
    return set(context.activity_names["ground_truth"]) ^ set(context.activity_names["detected"])

def case_only_in_one_log(context: aqudem.Context) -> Set[str]:
    return set(context.case_ids["ground_truth"]) ^ set(context.case_ids["detected"])


def _validate_two_set(two_set: aqudem.TwoSet) -> None:
    assert isinstance(two_set, aqudem.TwoSet)
    for key in ["tp", "tn", "d", "f", "ua", "uo", "i", "m", "oa", "oo",
                "p", "n", "t",
                "tpr", "tnr", "dr", "fr", "uar", "uor", "ir", "mr", "oar", "oor"]:
        assert isinstance(getattr(two_set, key), (int, float))
    assert two_set.tp + two_set.d + two_set.f + two_set.ua + two_set.uo == two_set.p
    assert two_set.tn + two_set.i + two_set.m + two_set.oa + two_set.oo == two_set.n
    assert round(two_set.p + two_set.n, 2) == round(two_set.t, 2)
    assert round(two_set.tpr + two_set.dr + two_set.fr + two_set.uar + two_set.uor, 4) - 1 < 0.001
    assert round(two_set.tnr + two_set.ir + two_set.mr + two_set.oar + two_set.oor, 4) - 1 < 0.001


def _validate_two_set_zero(two_set: aqudem.TwoSet) -> None:
    assert isinstance(two_set, aqudem.TwoSet)
    for key in ["tp", "f", "ua", "uo", "m", "oa", "oo",
                "tpr", "fr", "uar", "uor", "mr", "oar", "oor"]:
        assert getattr(two_set, key) == 0
    assert two_set.d > 0 or two_set.i > 0
    assert not (two_set.d > 0 and two_set.i > 0)
    assert two_set.dr > 0 or two_set.ir > 0
    assert not (two_set.dr > 0 and two_set.ir > 0)


def _validate_event_analysis(ea: aqudem.EventAnalysis) -> None:
    assert isinstance(ea, aqudem.EventAnalysis)
    for key in ["d", "f", "fm", "m", "c", "md", "fmd", "fd", "id",
                "total_gt_events", "total_det_events", "correct_events_per_log",
                "dr", "fr", "fmr", "mr", "cr_gt", "cr_det", "mdr", "fmdr", "fdr", "idr"]:
        assert isinstance(getattr(ea, key), (int, float))
    assert (ea.dr + ea.fr + ea.fmr + ea.mr + ea.cr_gt) - 1 < 0.001
    assert (ea.mdr + ea.fmdr + ea.fdr + ea.idr + ea.cr_det) - 1 < 0.001
    assert (ea.d + ea.f + ea.fm + ea.m + (ea.c / 2)) - ea.total_gt_events < 0.001
    assert (ea.md + ea.fd + ea.fmd + ea.id + (ea.c / 2)) - ea.total_det_events < 0.001


def _validate_event_analysis_zero(ea: aqudem.EventAnalysis) -> None:
    assert isinstance(ea, aqudem.EventAnalysis)
    for key in ["f", "fm", "m", "c", "md", "fmd", "fd",
                "correct_events_per_log",
                "fr", "fmr", "mr", "cr_gt", "cr_det", "mdr", "fmdr", "fdr"]:
        assert getattr(ea, key) == 0
    assert ea.d > 0 or ea.id > 0
    assert not (ea.d > 0 and ea.id > 0)
    assert ea.dr > 0 or ea.idr > 0
    assert not (ea.dr > 0 and ea.idr > 0)
    assert ea.total_gt_events > 0 or ea.total_det_events > 0
    assert not (ea.total_gt_events > 0 and ea.total_det_events > 0)


@pytest.fixture(scope="module", name='context')
def fixture_context(request: pytest.FixtureRequest) -> aqudem.Context:
    file1, file2 = request.param
    return aqudem.Context(os.path.join("tests", "resources", "experiment-logs", file1),
                          os.path.join("tests", "resources", "experiment-logs", file2))


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes")
], indirect=True)
def test_context_properties_3_20(context: aqudem.Context) -> None:
    assert isinstance(context.ground_truth, sf.FrameHE)
    assert isinstance(context.detected, sf.FrameHE)
    assert context.ground_truth.shape[0] <= 204
    assert context.ground_truth.shape[1] == 5
    for column in ["case:concept:name", "concept:name",
                   "lifecycle:transition", "time:timestamp", "concept:instance"]:
        assert column in context.ground_truth.columns
    assert context.detected.shape[0] <= 78
    assert context.detected.shape[1] == 5
    for column in ["case:concept:name", "concept:name", "lifecycle:transition",
                   "time:timestamp", "case:sampling_freq"]:
        assert column in context.detected.columns
    assert isinstance(context.activity_names, dict)
    assert isinstance(context.case_ids, dict)
    assert Counter(context.activity_names["ground_truth"]) == Counter(ACTIVIES_GT_03_20)
    assert Counter(context.activity_names["detected"]) == Counter(ACTIVITIES_DET_03_20)
    assert Counter(context.case_ids["ground_truth"]) == Counter(CASES_GT_03_20)
    assert Counter(context.case_ids["detected"]) == Counter(CASES_DET_03_20)


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes"),
    ("23_01_30_gt_camunda.xes", "23_01_30_det_firstlastlowlevel.xes"),
    ("23_02_06_gt_camunda.xes", "23_02_06_det_firstlastlowlevel.xes"),
    ("23_04_11_gt_camunda.xes", "23_04_11_det_firstlastlowlevel.xes"),
    ("23-01-02-03-04_gt_comb.xes", "23-01-02-03-04_det_comb.xes"),
], indirect=True)
def test_context_properties(context: aqudem.Context) -> None:
    assert isinstance(context.ground_truth, sf.FrameHE)
    assert isinstance(context.detected, sf.FrameHE)
    for column in ["case:concept:name", "concept:name",
                   "lifecycle:transition", "time:timestamp", "concept:instance"]:
        assert column in context.ground_truth.columns
    for column in ["case:concept:name", "concept:name", "lifecycle:transition",
                   "time:timestamp", "case:sampling_freq"]:
        assert column in context.detected.columns
    assert isinstance(context.activity_names, dict)
    assert isinstance(context.case_ids, dict)

@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes"),
    ("23_01_30_gt_camunda.xes", "23_01_30_det_firstlastlowlevel.xes"),
    ("23_02_06_gt_camunda.xes", "23_02_06_det_firstlastlowlevel.xes"),
    ("23_04_11_gt_camunda.xes", "23_04_11_det_firstlastlowlevel.xes"),
    ("23-01-02-03-04_gt_comb.xes", "23-01-02-03-04_det_comb.xes"),

], indirect=True)
def test_cross_correlation(context: aqudem.Context) -> None:
    cross_correlation = context.cross_correlation()
    assert isinstance(cross_correlation, tuple)
    assert isinstance(cross_correlation[0], (float, int))
    assert isinstance(cross_correlation[1], float)

    for act in get_set_all_activities(context):
        cross_correlation_act = context.cross_correlation(activity_name=act)
        assert isinstance(cross_correlation_act, tuple)
        assert isinstance(cross_correlation_act[0], (float, int))
        assert isinstance(cross_correlation_act[1], float)

    for cas in get_set_all_cases(context):
        cross_correlation_case = context.cross_correlation(case_id=cas)
        assert isinstance(cross_correlation_case, tuple)
        assert isinstance(cross_correlation_case[0], (float, int))
        assert isinstance(cross_correlation_case[1], float)

    for act in get_set_all_activities(context):
        for cas in get_set_all_cases(context):
            try:
                cross_correlation_act_case = context.cross_correlation(activity_name=act,
                                                                       case_id=cas)
                assert isinstance(cross_correlation_act_case, tuple)
                assert isinstance(cross_correlation_act_case[0], (float, int))
                assert isinstance(cross_correlation_act_case[1], float)
            except ValueError as e:
                assert "No metrics could be calculated for this combination" in str(e)

    # for activities that are only in one log, make sure that they are logically ZERO
    for act in act_only_in_one_log(context):
        cross_correlation_act = context.cross_correlation(activity_name=act)
        assert cross_correlation_act[0] == 0
        assert cross_correlation_act[1] == 0


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes"),
    ("23_01_30_gt_camunda.xes", "23_01_30_det_firstlastlowlevel.xes"),
    ("23_02_06_gt_camunda.xes", "23_02_06_det_firstlastlowlevel.xes"),
    ("23_04_11_gt_camunda.xes", "23_04_11_det_firstlastlowlevel.xes"),
    ("23-01-02-03-04_gt_comb.xes", "23-01-02-03-04_det_comb.xes"),

], indirect=True)
def test_two_set(context: aqudem.Context) -> None:
    two_set = context.two_set()
    _validate_two_set(two_set)

    for act in get_set_all_activities(context):
        two_set_act = context.two_set(activity_name=act)
        _validate_two_set(two_set_act)

    for cas in get_set_all_cases(context):
        two_set_case = context.two_set(case_id=cas)
        _validate_two_set(two_set_case)

    for act in get_set_all_activities(context):
        for cas in get_set_all_cases(context):
            try:
                two_set_act_case = context.two_set(activity_name=act, case_id=cas)
                _validate_two_set(two_set_act_case)
            except ValueError as e:
                assert "No metrics could be calculated for this combination" in str(e)

    for act in act_only_in_one_log(context):
        two_set_act = context.two_set(activity_name=act)
        _validate_two_set_zero(two_set_act)


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes"),
    ("23_01_30_gt_camunda.xes", "23_01_30_det_firstlastlowlevel.xes"),
    ("23_02_06_gt_camunda.xes", "23_02_06_det_firstlastlowlevel.xes"),
    ("23_04_11_gt_camunda.xes", "23_04_11_det_firstlastlowlevel.xes"),
    ("23-01-02-03-04_gt_comb.xes", "23-01-02-03-04_det_comb.xes"),

], indirect=True)
def test_event_analysis(context: aqudem.Context) -> None:
    ea = context.event_analysis()
    _validate_event_analysis(ea)

    for act in get_set_all_activities(context):
        ea_act = context.event_analysis(activity_name=act)
        _validate_event_analysis(ea_act)

    for cas in get_set_all_cases(context):
        ea_case = context.event_analysis(case_id=cas)
        _validate_event_analysis(ea_case)

    for act in get_set_all_activities(context):
        for cas in get_set_all_cases(context):
            try:
                ea_act_case = context.event_analysis(activity_name=act, case_id=cas)
                _validate_event_analysis(ea_act_case)
            except ValueError as e:
                assert "No metrics could be calculated for this combination" in str(e)

    for act in act_only_in_one_log(context):
        ea_act = context.event_analysis(activity_name=act)
        _validate_event_analysis_zero(ea_act)


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes"),
    ("23_01_30_gt_camunda.xes", "23_01_30_det_firstlastlowlevel.xes"),
    ("23_02_06_gt_camunda.xes", "23_02_06_det_firstlastlowlevel.xes"),
    ("23_04_11_gt_camunda.xes", "23_04_11_det_firstlastlowlevel.xes"),
    ("23-01-02-03-04_gt_comb.xes", "23-01-02-03-04_det_comb.xes"),

], indirect=True)
def test_damerau_levenshtein_distance(context: aqudem.Context) -> None:
    dld = context.damerau_levenshtein_distance()
    assert isinstance(dld[0], (int, float))
    assert isinstance(dld[1], float)
    assert dld[1] <= 1

    for cas in get_set_all_cases(context):
        dld_case = context.damerau_levenshtein_distance(case_id=cas)
        assert isinstance(dld_case[0], (int, float))
        assert isinstance(dld_case[1], float)
        assert dld_case[1] <= 1


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes"),
    ("23_01_30_gt_camunda.xes", "23_01_30_det_firstlastlowlevel.xes"),
    ("23_02_06_gt_camunda.xes", "23_02_06_det_firstlastlowlevel.xes"),
    ("23_04_11_gt_camunda.xes", "23_04_11_det_firstlastlowlevel.xes"),
    ("23-01-02-03-04_gt_comb.xes", "23-01-02-03-04_det_comb.xes"),

], indirect=True)
def test_levenshtein_distance(context: aqudem.Context) -> None:
    ld = context.levenshtein_distance()
    assert isinstance(ld[0], (int, float))
    assert isinstance(ld[1], float)
    assert ld[1] <= 1

    for cas in get_set_all_cases(context):
        ld_case = context.levenshtein_distance(case_id=cas)
        assert isinstance(ld_case[0], (int, float))
        assert isinstance(ld_case[1], float)
        assert ld_case[1] <= 1


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes")
], indirect=True)
def test_different_ordering_xes_same_result(context: aqudem.Context) -> None:
    context2 = aqudem.Context(os.path.join("tests",
                                           "resources",
                                           "23-03-20_gt_cam_ooo.xes"),
                              os.path.join("tests",
                                           "resources",
                                           "23-03-20_det_firstlastlowlevel_ooo.xes"))
    assert context.activity_names == context2.activity_names
    assert context.case_ids == context2.case_ids
    assert context.cross_correlation() == context2.cross_correlation()
    assert context.two_set() == context2.two_set()
    assert context.event_analysis() == context2.event_analysis()
    assert context.damerau_levenshtein_distance() == context2.damerau_levenshtein_distance()
    assert context.levenshtein_distance() == context2.levenshtein_distance()


@pytest.mark.parametrize("context", [
    ("23-03-20_gt_camunda.xes", "23-03-20_det_firstlastlowlevel.xes")
], indirect=True)
def test_wrong_case_or_activity_raises_exception(context: aqudem.Context) -> None:
    with pytest.raises(ValueError):
        context.two_set(activity_name="wrong_activity_name")
    with pytest.raises(ValueError):
        context.two_set(case_id="wrong_case_id")


@pytest.mark.parametrize("context", [
    ("23_04_11_gt_camunda.xes", "23_04_11_det_firstlastlowlevel.xes")
], indirect=True)
def test_no_duration_activities_removed(context: aqudem.Context) -> None:
    """ Test that activities with no duration are removed. """
    with pytest.raises(ValueError) as e:
        context.cross_correlation(activity_name="Read Color")
    assert "The activity name 'Read Color' is not in the event logs." in str(e)
