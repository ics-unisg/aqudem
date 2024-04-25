""" Testing the aqudem package end-to-end. """
import os
import pytest
import static_frame as sf
import aqudem

ACTIVIES_GT = ['OV Burn', 'Sorting Machine sort', 'WT Transport', 'Calibrate VGR',
               'Get Workpiece from Pickup Station', 'Pickup and transport to sink',
               'Pickup and transport to Oven', 'Unload from HBW', 'Store Workpiece in HBW',
               'Calibrate HBW', 'Start Milling Machine', 'Move to DPS']
ACTIVITIES_DET = ['WT Transport', 'Get Workpiece from Pickup Station',
                  'Store Workpiece in HBW', 'Calibrate HBW', 'Read Color', 'Move to DPS']
CASES_GT = ['case1']
CASES_DET = ['case1']
act_only_in_one_log = set(ACTIVIES_GT) ^ set(ACTIVITIES_DET)
case_only_in_one_log = set(CASES_GT) ^ set(CASES_DET)


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
def fixture_context() -> aqudem.Context:
    return aqudem.Context(os.path.join("tests", "resources", "23-03-20_gt_cam.xes"),
                          os.path.join("tests", "resources", "23-03-20_det_firstlastlowlevel.xes"))


def test_context_properties(context: aqudem.Context) -> None:
    assert isinstance(context.ground_truth, sf.FrameHE)
    assert isinstance(context.detected, sf.FrameHE)
    assert context.ground_truth.shape[0] <= 204
    assert context.ground_truth.shape[1] == 6
    for column in ["case:concept:name", "case:sampling_freq", "concept:name",
                   "lifecycle:transition", "time:timestamp", "concept:instance"]:
        assert column in context.ground_truth.columns
    assert context.detected.shape[0] <= 78
    assert context.detected.shape[1] == 5
    for column in ["case:concept:name", "concept:name", "lifecycle:transition",
                   "time:timestamp", "case:sampling_freq"]:
        assert column in context.detected.columns
    assert isinstance(context.activity_names, dict)
    assert isinstance(context.case_ids, dict)


def test_cross_correlation(context: aqudem.Context) -> None:
    cross_correlation = context.cross_correlation()
    assert isinstance(cross_correlation, tuple)
    assert isinstance(cross_correlation[0], (float, int))
    assert isinstance(cross_correlation[1], float)

    for act in set(ACTIVIES_GT + ACTIVITIES_DET):
        cross_correlation_act = context.cross_correlation(activity_name=act)
        assert isinstance(cross_correlation_act, tuple)
        assert isinstance(cross_correlation_act[0], (float, int))
        assert isinstance(cross_correlation_act[1], float)

    for cas in set(CASES_GT + CASES_DET):
        cross_correlation_case = context.cross_correlation(case_id=cas)
        assert isinstance(cross_correlation_case, tuple)
        assert isinstance(cross_correlation_case[0], (float, int))
        assert isinstance(cross_correlation_case[1], float)

    for act in set(ACTIVIES_GT + ACTIVITIES_DET):
        for cas in set(CASES_GT + CASES_DET):
            cross_correlation_act_case = context.cross_correlation(activity_name=act,
                                                                   case_id=cas)
            assert isinstance(cross_correlation_act_case, tuple)
            assert isinstance(cross_correlation_act_case[0], (float, int))
            assert isinstance(cross_correlation_act_case[1], float)

    # for activities that are only in one log, make sure that they are logically ZERO
    for act in act_only_in_one_log:
        cross_correlation_act = context.cross_correlation(activity_name=act)
        assert cross_correlation_act[0] == 0
        assert cross_correlation_act[1] == 0

    # for cases that are only in one log, make sure that they are logically ZERO
    for cas in case_only_in_one_log:
        cross_correlation_case = context.cross_correlation(case_id=cas)
        assert cross_correlation_case[0] == 0
        assert cross_correlation_case[1] == 0

    # for tha case + act query from above, it should also be logically ZERO
    for act in act_only_in_one_log:
        for cas in case_only_in_one_log:
            cross_correlation_act_case = context.cross_correlation(activity_name=act,
                                                                   case_id=cas)
            assert cross_correlation_act_case[0] == 0
            assert cross_correlation_act_case[1] == 0


def test_two_set(context: aqudem.Context) -> None:
    two_set = context.two_set()
    _validate_two_set(two_set)

    for act in set(ACTIVIES_GT + ACTIVITIES_DET):
        two_set_act = context.two_set(activity_name=act)
        _validate_two_set(two_set_act)

    for cas in set(CASES_GT + CASES_DET):
        two_set_case = context.two_set(case_id=cas)
        _validate_two_set(two_set_case)

    for act in set(ACTIVIES_GT + ACTIVITIES_DET):
        for cas in set(CASES_GT + CASES_DET):
            two_set_act_case = context.two_set(activity_name=act, case_id=cas)
            _validate_two_set(two_set_act_case)

    for act in act_only_in_one_log:
        two_set_act = context.two_set(activity_name=act)
        _validate_two_set_zero(two_set_act)

    for cas in case_only_in_one_log:
        two_set_case = context.two_set(case_id=cas)
        _validate_two_set_zero(two_set_case)

    for act in act_only_in_one_log:
        for cas in case_only_in_one_log:
            two_set_act_case = context.two_set(activity_name=act, case_id=cas)
            _validate_two_set_zero(two_set_act_case)


def test_event_analysis(context: aqudem.Context) -> None:
    ea = context.event_analysis()
    _validate_event_analysis(ea)

    for act in set(ACTIVIES_GT + ACTIVITIES_DET):
        ea_act = context.event_analysis(activity_name=act)
        _validate_event_analysis(ea_act)

    for cas in set(CASES_GT + CASES_DET):
        ea_case = context.event_analysis(case_id=cas)
        _validate_event_analysis(ea_case)

    for act in set(ACTIVIES_GT + ACTIVITIES_DET):
        for cas in set(CASES_GT + CASES_DET):
            ea_act_case = context.event_analysis(activity_name=act, case_id=cas)
            _validate_event_analysis(ea_act_case)

    for act in act_only_in_one_log:
        ea_act = context.event_analysis(activity_name=act)
        _validate_event_analysis_zero(ea_act)

    for cas in case_only_in_one_log:
        ea_case = context.event_analysis(case_id=cas)
        _validate_event_analysis_zero(ea_case)

    for act in act_only_in_one_log:
        for cas in case_only_in_one_log:
            ea_act_case = context.event_analysis(activity_name=act, case_id=cas)
            _validate_event_analysis_zero(ea_act_case)


def test_damerau_levenshtein_distance(context: aqudem.Context) -> None:
    dld = context.damerau_levenshtein_distance()
    assert isinstance(dld[0], (int, float))
    assert isinstance(dld[1], float)
    assert dld[1] <= 1

    for cas in set(CASES_GT + CASES_DET):
        dld_case = context.damerau_levenshtein_distance(case_id=cas)
        assert isinstance(dld_case[0], (int, float))
        assert isinstance(dld_case[1], float)
        assert dld_case[1] <= 1

    for cas in case_only_in_one_log:
        dld_case = context.damerau_levenshtein_distance(case_id=cas)
        assert dld_case[0] > 0
        assert dld_case[1] > 0


def test_levenshtein_distance(context: aqudem.Context) -> None:
    ld = context.levenshtein_distance()
    assert isinstance(ld[0], (int, float))
    assert isinstance(ld[1], float)
    assert ld[1] <= 1

    for cas in set(CASES_GT + CASES_DET):
        ld_case = context.levenshtein_distance(case_id=cas)
        assert isinstance(ld_case[0], (int, float))
        assert isinstance(ld_case[1], float)
        assert ld_case[1] <= 1

    for cas in case_only_in_one_log:
        ld_case = context.levenshtein_distance(case_id=cas)
        assert ld_case[0] > 0
        assert ld_case[1] > 0


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


def test_wrong_case_or_activity_raises_exception(context: aqudem.Context) -> None:
    with pytest.raises(ValueError):
        context.two_set(activity_name="wrong_activity_name")
    with pytest.raises(ValueError):
        context.two_set(case_id="wrong_case_id")
