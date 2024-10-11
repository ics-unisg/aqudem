"""Tests for the two_set_helper module."""
import os
from dataclasses import fields
import aqudem
from aqudem.two_set_helper import (_two_set, TwoSet, _two_set_by_activity_case)
from .mocks.logs import (ground_truth_ten_eighteen, detected_ten_eighteen,
                         ground_truth_ten_eleven, detected_ten_eleven,
                         start_end_series_ten_eleven, start_end_series_ten_eighteen)

rate_props = ["uar", "oar", "tpr", "fr", "uor", "tnr", "oor", "ir", "dr", "mr"]


def verify_single_act_rates_ten_eighteen(result: TwoSet) -> None:
    assert result.uar == round(900 / 21601, 4)
    assert result.oar == round(900 / 7200, 4)
    assert result.tpr == round(13500 / 21601, 4)
    assert result.fr == round(3600 / 21601, 4)
    assert result.oor == round(3600 / 7200, 4)
    assert result.tnr == round(2700 / 7200, 4)
    assert result.uor == round(3601 / 21601, 4)
    assert result.ir == 0.0
    assert result.dr == 0.0
    assert result.mr == 0.0
    sum_metr = 0.0
    for field in rate_props:
        sum_metr += getattr(result, field)
    assert abs(sum_metr - 2.0) < 0.001


def verify_single_act_metrics_ten_eighteen(result: TwoSet) -> None:
    assert isinstance(result, TwoSet)
    assert result.ua == 900
    assert result.tp == 13500
    assert result.f == 3600
    assert result.oo == 3600
    assert result.oa == 900
    assert result.tn == 2700
    assert result.uo == 3601
    assert result.i == 0
    assert result.d == 0
    assert result.m == 0
    assert result.p == 21601
    assert result.n == 7200
    sum_metr = 0
    for field in fields(result):
        sum_metr += getattr(result, field.name)
    assert sum_metr == 28801


def verify_two_set_metrics_ten_eleven(result: TwoSet) -> None:
    assert isinstance(result, TwoSet)
    assert result.oa == 600
    assert result.tp == 1080
    assert result.f == 300
    assert result.uo == 300
    assert result.tn == 540
    assert result.oo == 421
    assert result.ua == 300
    assert result.i == 60
    assert result.d == 0
    assert result.m == 0
    assert result.t == 3601
    assert result.p == 1980
    assert result.n == 1621


def verify_two_set_rates_ten_eleven(result: TwoSet) -> None:
    assert isinstance(result, TwoSet)
    assert result.oar == round(600 / 1621, 4)
    assert result.tpr == round(1080 / 1980, 4)
    assert result.fr == round(300 / 1980, 4)
    assert result.uor == round(300 / 1980, 4)
    assert result.tnr == round(540 / 1621, 4)
    assert result.oor == round(421 / 1621, 4)
    assert result.uar == round(300 / 1980, 4)
    assert result.ir == round(60 / 1621, 4)
    assert result.dr == 0.0
    assert result.mr == 0.0


def verify_rates_avg_ten_eleven_eighteen(result: TwoSet) -> None:
    assert isinstance(result, TwoSet)
    assert result.uar == 0.0572
    assert result.oar == 0.0989
    assert result.tpr == 0.3843
    assert result.fr == 0.1041
    assert result.uor == 0.1041
    assert result.tnr == 0.1218
    assert result.oor == 0.121
    assert result.ir == 0.0083
    assert result.dr == 0.0
    assert result.mr == 0.0
    sum_metr = 0.0
    for field in rate_props:
        sum_metr += getattr(result, field)
    assert abs(sum_metr - 2.0) < 0.001


def verify_metrics_avg_ten_eleven_eighteen(result: TwoSet) -> None:
    assert isinstance(result, TwoSet)
    assert result.ua == 600
    assert result.tp == 7290
    assert result.f == 1950
    assert result.oo == 2010
    assert result.oa == 750
    assert result.tn == 1620
    assert result.uo == 1950
    assert result.i == 30
    assert result.d == 0
    assert result.m == 0


def test_two_set() -> None:
    result = _two_set(ground_truth_ten_eighteen,
                      detected_ten_eighteen,
                      start_end_series_ten_eighteen,
                      1)
    verify_single_act_metrics_ten_eighteen(result)

    result = _two_set(ground_truth_ten_eleven,
                      detected_ten_eleven,
                      start_end_series_ten_eleven,
                      1)
    verify_two_set_metrics_ten_eleven(result)


def test_two_set_rates() -> None:
    result = _two_set(ground_truth_ten_eighteen,
                      detected_ten_eighteen,
                      start_end_series_ten_eighteen,
                      1)
    verify_single_act_rates_ten_eighteen(result)

    result = _two_set(ground_truth_ten_eleven,
                      detected_ten_eleven,
                      start_end_series_ten_eleven,
                      1)
    verify_two_set_rates_ten_eleven(result)


def test_two_set_two_herz() -> None:
    result = _two_set(ground_truth_ten_eleven,
                      detected_ten_eleven,
                      start_end_series_ten_eleven,
                      2)
    assert isinstance(result, TwoSet)
    assert result.oa == 1200
    assert result.tp == 2160
    assert result.f == 600
    assert result.uo == 600
    assert result.tn == 1080
    assert result.oo == 841
    assert result.ua == 600
    assert result.i == 120
    assert result.d == 0
    assert result.m == 0
    assert result.t == 7201
    assert result.p == 3960
    assert result.n == 3241


def test_two_set_rates_two_hertz() -> None:
    result = _two_set(ground_truth_ten_eleven,
                      detected_ten_eleven,
                      start_end_series_ten_eleven,
                      2)
    assert isinstance(result, TwoSet)
    assert result.oar == round(1200 / 3241, 4)
    assert result.tpr == round(2160 / 3960, 4)
    assert result.fr == round(600 / 3960, 4)
    assert result.uor == round(600 / 3960, 4)
    assert result.tnr == round(1080 / 3241, 4)
    assert result.oor == round(841 / 3241, 4)
    assert result.uar == round(600 / 3960, 4)
    assert result.ir == round(120 / 3241, 4)
    assert result.dr == 0.0
    assert result.mr == 0.0


def test_two_set_by_activity_only_one_act_in_log() -> None:
    result_a = _two_set_by_activity_case(ground_truth_ten_eighteen,
                                         detected_ten_eighteen,
                                         1,
                                         "*",
                                         "1",
                                         start_end_series_ten_eighteen)
    verify_single_act_metrics_ten_eighteen(result_a)


def test_two_set_rates_by_activity_only_one_act_in_log() -> None:
    result_a = _two_set_by_activity_case(ground_truth_ten_eighteen,
                                         detected_ten_eighteen,
                                         1,
                                         "*",
                                         "1",
                                         start_end_series_ten_eighteen)
    verify_single_act_rates_ten_eighteen(result_a)


# pylint: disable=too-many-statements
def test_two_set_via_context_one_case_one_activity() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity A", case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tp == 780
    assert res.d == 0
    assert res.f == 60
    assert res.ua == 0
    assert res.uo == 120
    assert res.tn == 2281
    assert res.i == 0
    assert res.m == 0
    assert res.oa == 0
    assert res.oo == 300
    assert res.p == 960
    assert res.n == 2581

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity B", case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tp == 390
    assert res.d == 0
    assert res.f == 0
    assert res.ua == 0
    assert res.uo == 0
    assert res.tn == 3001
    assert res.i == 0
    assert res.m == 30
    assert res.oa == 120
    assert res.oo == 0
    assert res.p == 390
    assert res.n == 3151

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity C", case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tp == 421
    assert res.d == 240
    assert res.f == 0
    assert res.ua == 120
    assert res.uo == 0
    assert res.tn == 2760
    assert res.i == 0
    assert res.m == 0
    assert res.oa == 0
    assert res.oo == 0
    assert res.p == 781
    assert res.n == 2760

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity A", case_id="ExampleTrace2")
    assert isinstance(res, TwoSet)
    assert res.tp == 0
    assert res.d == 120
    assert res.f == 0
    assert res.ua == 0
    assert res.uo == 0
    assert res.tn == 241
    assert res.i == 180
    assert res.m == 0
    assert res.oa == 0
    assert res.oo == 0
    assert res.p == 120
    assert res.n == 421

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity B", case_id="ExampleTrace2")
    assert isinstance(res, TwoSet)
    assert res.tp == 300
    assert res.d == 0
    assert res.f == 60
    assert res.ua == 0
    assert res.uo == 61
    assert res.tn == 0
    assert res.i == 0
    assert res.m == 60
    assert res.oa == 60
    assert res.oo == 0
    assert res.p == 421
    assert res.n == 120


# pylint: disable=too-many-statements
def test_two_set_rates_via_context_one_case_one_activity() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity A", case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tpr == round(780 / 960, 4)
    assert res.dr == 0.0
    assert res.fr == round(60 / 960, 4)
    assert res.uar == 0.0
    assert res.uor == round(120 / 960, 4)
    assert res.tnr == round(2281 / 2581, 4)
    assert res.ir == 0.0
    assert res.mr == 0.0
    assert res.oar == 0.0
    assert res.oor == round(300 / 2581, 4)
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity B", case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tpr == round(390 / 390, 4)
    assert res.dr == 0.0
    assert res.fr == 0.0
    assert res.uar == 0.0
    assert res.uor == 0.0
    assert res.tnr == round(3001 / 3151, 4)
    assert res.ir == 0.0
    assert res.mr == round(30 / 3151, 4)
    assert res.oar == round(120 / 3151, 4)
    assert res.oor == 0.0
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity C", case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tpr == round(421 / 781, 4)
    assert res.dr == round(240 / 781, 4)
    assert res.fr == 0.0
    assert res.uar == round(120 / 781, 4)
    assert res.uor == 0.0
    assert res.tnr == round(2760 / 2760, 4)
    assert res.ir == 0.0
    assert res.mr == 0.0
    assert res.oar == 0.0
    assert res.oor == 0.0
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity A", case_id="ExampleTrace2")
    assert isinstance(res, TwoSet)
    assert res.tpr == 0.0
    assert res.dr == round(120 / 120, 4)
    assert res.fr == 0.0
    assert res.uar == 0.0
    assert res.uor == 0.0
    assert res.tnr == round(241 / 421, 4)
    assert res.ir == round(180 / 421, 4)
    assert res.mr == 0.0
    assert res.oar == 0.0
    assert res.oor == 0.0
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001

    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity B", case_id="ExampleTrace2")
    assert isinstance(res, TwoSet)
    assert res.tpr == round(300 / 421, 4)
    assert res.dr == 0.0
    assert res.fr == round(60 / 421, 4)
    assert res.uar == 0.0
    assert res.uor == round(61 / 421, 4)
    assert res.tnr == 0.0
    assert res.ir == 0.0
    assert res.mr == round(60 / 120, 4)
    assert res.oar == round(60 / 120, 4)
    assert res.oor == 0.0
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001


def test_context_two_set_by_activty() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity A")
    assert isinstance(res, TwoSet)
    assert res.tp == round((780 + 0) / 2, 4)
    assert res.d == round((0 + 120) / 2, 4)
    assert res.f == round((60 + 0) / 2, 4)
    assert res.ua == round((0 + 0) / 2, 4)
    assert res.uo == round((120 + 0) / 2, 4)
    assert res.tn == round((2281 + 241) / 2, 4)
    assert res.i == round((0 + 180) / 2, 4)
    assert res.m == round((0 + 0) / 2, 4)
    assert res.oa == round((0 + 0) / 2, 4)
    assert res.oo == round((300 + 0) / 2, 4)
    assert res.p == round((960 + 120) / 2, 4)
    assert res.n == round((2581 + 421) / 2, 4)
    res = context.two_set(activity_name="Activity B")
    assert isinstance(res, TwoSet)
    assert res.tp == round((390 + 300) / 2, 4)
    assert res.d == round((0 + 0) / 2, 4)
    assert res.f == round((0 + 60) / 2, 4)
    assert res.ua == round((0 + 0) / 2, 4)
    assert res.uo == round((0 + 61) / 2, 4)
    assert res.tn == round((3001 + 0) / 2, 4)
    assert res.i == round((0 + 0) / 2, 4)
    assert res.m == round((30 + 60) / 2, 4)
    assert res.oa == round((120 + 60) / 2, 4)
    assert res.oo == round((0 + 0) / 2, 4)
    assert res.p == round((390 + 421) / 2, 4)
    assert res.n == round((3151 + 120) / 2, 4)
    res = context.two_set(activity_name="Activity C")
    assert isinstance(res, TwoSet)
    assert res.tp == 421
    assert res.d == 240
    assert res.f == 0
    assert res.ua == 120
    assert res.uo == 0
    assert res.tn == 2760
    assert res.i == 0
    assert res.m == 0
    assert res.oa == 0
    assert res.oo == 0
    assert res.p == 781
    assert res.n == 2760


def test_context_two_set_by_case() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tp == round((780 + 390 + 421) / 3, 4)
    assert res.d == round((0 + 0 + 240) / 3, 4)
    assert res.f == round((60 + 0 + 0) / 3, 4)
    assert res.ua == round((0 + 0 + 120) / 3, 4)
    assert res.uo == round((120 + 0 + 0) / 3, 4)
    assert res.tn == round((2281 + 3001 + 2760) / 3, 4)
    assert res.i == round((0 + 0 + 0) / 3, 4)
    assert res.m == round((0 + 30 + 0) / 3, 4)
    assert res.oa == round((0 + 120 + 0) / 3, 4)
    assert res.oo == round((300 + 0 + 0) / 3, 4)
    assert res.p == round((960 + 390 + 781) / 3, 4)
    assert res.n == round((2581 + 3151 + 2760) / 3, 4)
    res = context.two_set(case_id="ExampleTrace2")
    assert isinstance(res, TwoSet)
    assert res.tp == round((0 + 300) / 2, 4)
    assert res.d == round((120 + 0) / 2, 4)
    assert res.f == round((0 + 60) / 2, 4)
    assert res.ua == round((0 + 0) / 2, 4)
    assert res.uo == round((0 + 61) / 2, 4)
    assert res.tn == round((241 + 0) / 2, 4)
    assert res.i == round((180 + 0) / 2, 4)
    assert res.m == round((0 + 60) / 2, 4)
    assert res.oa == round((0 + 60) / 2, 4)
    assert res.oo == round((0 + 0) / 2, 4)


def test_context_two_set_by_activty_case() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set()
    assert isinstance(res, TwoSet)
    assert res.tp == round((780 + 390 + 421 + 0 + 300) / 5, 4)
    assert res.d == round((0 + 0 + 240 + 120 + 0) / 5, 4)
    assert res.f == round((60 + 0 + 0 + 0 + 60) / 5, 4)
    assert res.ua == round((0 + 0 + 120 + 0 + 0) / 5, 4)
    assert res.uo == round((120 + 0 + 0 + 0 + 61) / 5, 4)
    assert res.tn == round((2281 + 3001 + 2760 + 241 + 0) / 5, 4)
    assert res.i == round((0 + 0 + 0 + 180 + 0) / 5, 4)
    assert res.m == round((0 + 30 + 0 + 0 + 60) / 5, 4)
    assert res.oa == round((0 + 120 + 0 + 0 + 60) / 5, 4)
    assert res.oo == round((300 + 0 + 0 + 0 + 0) / 5, 4)
    assert res.p == round((960 + 390 + 781 + 120 + 421) / 5, 4)
    assert res.n == round((2581 + 3151 + 2760 + 421 + 120) / 5, 4)


def test_context_two_set_rates_by_activty() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(activity_name="Activity A")
    assert isinstance(res, TwoSet)
    assert res.tpr == round((780 + 0) / (960 + 120), 4)
    assert res.dr == round((0 + 120) / (960 + 120), 4)
    assert res.fr == round((60 + 0) / (960 + 120), 4)
    assert res.uar == round((0 + 0) / (960 + 120), 4)
    assert res.uor == round((120 + 0) / (960 + 120), 4)
    assert res.tnr == round((2281 + 241) / (2581 + 421), 4)
    assert res.ir == round((0 + 180) / (2581 + 421), 4)
    assert res.mr == round((0 + 0) / (2581 + 421), 4)
    assert res.oar == round((0 + 0) / (2581 + 421), 4)
    assert res.oor == round((300 + 0) / (2581 + 421), 4)
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001
    res = context.two_set(activity_name="Activity B")
    assert isinstance(res, TwoSet)
    assert res.tpr == round((390 + 300) / (390 + 421), 4)
    assert res.dr == round((0 + 0) / (390 + 421), 4)
    assert res.fr == round((0 + 60) / (390 + 421), 4)
    assert res.uar == round((0 + 0) / (390 + 421), 4)
    assert res.uor == round((0 + 61) / (390 + 421), 4)
    assert res.tnr == round((3001 + 0) / (3151 + 120), 4)
    assert res.ir == round((0 + 0) / (3151 + 120), 4)
    assert res.mr == round((30 + 60) / (3151 + 120), 4)
    assert res.oar == round((120 + 60) / (3151 + 120), 4)
    assert res.oor == round((0 + 0) / (3151 + 120), 4)
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001
    res = context.two_set(activity_name="Activity C")
    assert isinstance(res, TwoSet)
    assert res.tpr == round(421 / 781, 4)
    assert res.dr == round(240 / 781, 4)
    assert res.fr == 0.0
    assert res.uar == round(120 / 781, 4)
    assert res.uor == 0.0
    assert res.tnr == round(2760 / 2760, 4)
    assert res.ir == 0.0
    assert res.mr == 0.0
    assert res.oar == 0.0
    assert res.oor == 0.0
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001


def test_context_two_set_rates_by_case() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set(case_id="ExampleTrace1")
    assert isinstance(res, TwoSet)
    assert res.tpr == round((780 + 390 + 421) / (960 + 390 + 781), 4)
    assert res.dr == round((0 + 0 + 240) / (960 + 390 + 781), 4)
    assert res.fr == round((60 + 0 + 0) / (960 + 390 + 781), 4)
    assert res.uar == round((0 + 0 + 120) / (960 + 390 + 781), 4)
    assert res.uor == round((120 + 0 + 0) / (960 + 390 + 781), 4)
    assert res.tnr == round((2281 + 3001 + 2760) / (2581 + 3151 + 2760), 4)
    assert res.ir == round((0 + 0 + 0) / (2581 + 3151 + 2760), 4)
    assert res.mr == round((0 + 30 + 0) / (2581 + 3151 + 2760), 4)
    assert res.oar == round((0 + 120 + 0) / (2581 + 3151 + 2760), 4)
    assert res.oor == round((300 + 0 + 0) / (2581 + 3151 + 2760), 4)
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001
    res = context.two_set(case_id="ExampleTrace2")
    assert isinstance(res, TwoSet)
    assert res.tpr == round((0 + 300) / (120 + 421), 4)
    assert res.dr == round((120 + 0) / (120 + 421), 4)
    assert res.fr == round((0 + 60) / (120 + 421), 4)
    assert res.uar == round((0 + 0) / (120 + 421), 4)
    assert res.uor == round((0 + 61) / (120 + 421), 4)
    assert res.tnr == round((241 + 0) / (421 + 120), 4)
    assert res.ir == round((180 + 0) / (421 + 120), 4)
    assert res.mr == round((0 + 60) / (421 + 120), 4)
    assert res.oar == round((0 + 60) / (421 + 120), 4)
    assert res.oor == round((0 + 0) / (421 + 120), 4)
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001


def test_context_two_set_rates_by_activty_case() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set()
    assert isinstance(res, TwoSet)
    assert res.tpr == round((780 + 390 + 421 + 0 + 300) / (960 + 390 + 781 + 120 + 421), 4)
    assert res.dr == round((0 + 0 + 240 + 120 + 0) / (960 + 390 + 781 + 120 + 421), 4)
    assert res.fr == round((60 + 0 + 0 + 0 + 60) / (960 + 390 + 781 + 120 + 421), 4)
    assert res.uar == round((0 + 0 + 120 + 0 + 0) / (960 + 390 + 781 + 120 + 421), 4)
    assert res.uor == round((120 + 0 + 0 + 0 + 61) / (960 + 390 + 781 + 120 + 421), 4)
    assert res.tnr == round((2281 + 3001 + 2760 + 241 + 0) / (2581 + 3151 + 2760 + 421 + 120), 4)
    assert res.ir == round((0 + 0 + 0 + 180 + 0) / (2581 + 3151 + 2760 + 421 + 120), 4)
    assert res.mr == round((0 + 30 + 0 + 0 + 60) / (2581 + 3151 + 2760 + 421 + 120), 4)
    assert res.oar == round((0 + 120 + 0 + 60 + 0) / (2581 + 3151 + 2760 + 421 + 120), 4)
    assert res.oor == round((300 + 0 + 0 + 0 + 0) / (2581 + 3151 + 2760 + 421 + 120), 4)
    summed = 0.0
    for field in rate_props:
        summed += getattr(res, field)
    assert abs(summed - 2.0) < 0.001


def test_two_set_recall_precision_f1_balacc() -> None:
    context = aqudem.Context(os.path.join("tests", "resources", "ground_truth.xes"),
                             os.path.join("tests", "resources", "detected.xes"))
    res = context.two_set()
    assert isinstance(res, TwoSet)
    assert res.tpr == res.recall
    # merely check that the others do not raise an exception and that they are within
    # the range [0, 1]
    assert 0 <= res.recall <= 1
    assert 0 <= res.precision <= 1
    assert 0 <= res.f1 <= 1
    assert 0 <= res.balanced_accuracy <= 1
