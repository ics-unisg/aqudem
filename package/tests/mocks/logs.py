from datetime import datetime
import static_frame as sf

ground_truth_ten_eleven = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 5), datetime(2021, 1, 1, 10, 25),
                       datetime(2021, 1, 1, 10, 35), datetime(2021, 1, 1, 10, 38),
                       datetime(2021, 1, 1, 10, 45), datetime(2021, 1, 1, 10, 55)],
})
detected_ten_eleven = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete", "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 10, 10),
                       datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 10, 20),
                       datetime(2021, 1, 1, 10, 30), datetime(2021, 1, 1, 10, 40),
                        datetime(2021, 1, 1, 10, 41), datetime(2021, 1, 1, 10, 42),
                       datetime(2021, 1, 1, 10, 50), datetime(2021, 1, 1, 11, 0)],
})


ground_truth_ten_eighteen = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 12, 0),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 15, 0),
                       datetime(2021, 1, 1, 16, 0), datetime(2021, 1, 1, 18, 0)]
})
detected_ten_eighteen = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete",
                             "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 11, 0),
                       datetime(2021, 1, 1, 11, 30), datetime(2021, 1, 1, 12, 30),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 14, 0),
                       datetime(2021, 1, 1, 14, 30), datetime(2021, 1, 1, 15, 30),
                       datetime(2021, 1, 1, 15, 45), datetime(2021, 1, 1, 17, 0)]
})

ground_truth_mult_act_t_e = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "B", "B", "B", "B"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete", "start", "complete",
                             "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 12, 0),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 15, 0),
                       datetime(2021, 1, 1, 16, 0), datetime(2021, 1, 1, 18, 0),
                       datetime(2021, 1, 2, 10, 0), datetime(2021, 1, 2, 12, 0),
                       datetime(2021, 1, 2, 13, 0), datetime(2021, 1, 2, 15, 0)]
})
detected_mult_act_t_e = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "B", "B", "B", "B"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete",
                             "start", "complete", "start", "complete", "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 11, 0),
                       datetime(2021, 1, 1, 11, 30), datetime(2021, 1, 1, 12, 30),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 14, 0),
                       datetime(2021, 1, 1, 14, 30), datetime(2021, 1, 1, 15, 30),
                       datetime(2021, 1, 1, 15, 45), datetime(2021, 1, 1, 17, 0),
                       datetime(2021, 1, 2, 10, 15), datetime(2021, 1, 2, 11, 0),
                       datetime(2021, 1, 2, 11, 30), datetime(2021, 1, 2, 12, 30)]
})

ground_truth_mixed_activity = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "B", "B", "B", "B", "B", "B"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete", "start", "complete", "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 5), datetime(2021, 1, 1, 10, 25),
                       datetime(2021, 1, 1, 10, 35), datetime(2021, 1, 1, 10, 38),
                       datetime(2021, 1, 1, 10, 45), datetime(2021, 1, 1, 10, 55),
                       datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 12, 0),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 15, 0),
                       datetime(2021, 1, 1, 16, 0), datetime(2021, 1, 1, 18, 0)],
})
detected_mixed_activity = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1",
                          "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A",
                     "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete", "start", "complete", "start", "complete",
                             "start", "complete", "start", "complete", "start", "complete",
                             "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 10, 10),
                       datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 10, 20),
                       datetime(2021, 1, 1, 10, 30), datetime(2021, 1, 1, 10, 40),
                        datetime(2021, 1, 1, 10, 41), datetime(2021, 1, 1, 10, 42),
                       datetime(2021, 1, 1, 10, 50), datetime(2021, 1, 1, 11, 0),
                       datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 11, 0),
                       datetime(2021, 1, 1, 11, 30), datetime(2021, 1, 1, 12, 30),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 14, 0),
                       datetime(2021, 1, 1, 14, 30), datetime(2021, 1, 1, 15, 30),
                       datetime(2021, 1, 1, 15, 45), datetime(2021, 1, 1, 17, 0)],
})


ground_truth_mixed_case = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "2", "2", "2", "2", "2", "2"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete", "start", "complete", "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 5), datetime(2021, 1, 1, 10, 25),
                       datetime(2021, 1, 1, 10, 35), datetime(2021, 1, 1, 10, 38),
                       datetime(2021, 1, 1, 10, 45), datetime(2021, 1, 1, 10, 55),
                       datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 12, 0),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 15, 0),
                       datetime(2021, 1, 1, 16, 0), datetime(2021, 1, 1, 18, 0)],
})
detected_mixed_case = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1",
                          "2", "2", "2", "2", "2", "2", "2", "2", "2", "2"],
    "concept:name": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A",
                     "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
    "lifecycle:transition": ["start", "complete", "start", "complete", "start", "complete", "start", "complete", "start", "complete",
                             "start", "complete", "start", "complete", "start", "complete",
                             "start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 10, 10),
                       datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 10, 20),
                       datetime(2021, 1, 1, 10, 30), datetime(2021, 1, 1, 10, 40),
                        datetime(2021, 1, 1, 10, 41), datetime(2021, 1, 1, 10, 42),
                       datetime(2021, 1, 1, 10, 50), datetime(2021, 1, 1, 11, 0),
                       datetime(2021, 1, 1, 10, 15), datetime(2021, 1, 1, 11, 0),
                       datetime(2021, 1, 1, 11, 30), datetime(2021, 1, 1, 12, 30),
                       datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 14, 0),
                       datetime(2021, 1, 1, 14, 30), datetime(2021, 1, 1, 15, 30),
                       datetime(2021, 1, 1, 15, 45), datetime(2021, 1, 1, 17, 0)],
})


_start_end_ten_eleven = {"1": (datetime(2021, 1, 1, 10, 0),
                               datetime(2021, 1, 1, 11, 0))}
start_end_series_ten_eleven = sf.SeriesHE.from_dict(_start_end_ten_eleven)


_start_end_ten_eighteen = {"1": (datetime(2021, 1, 1, 10, 0),
                                 datetime(2021, 1, 1, 18, 0))}
start_end_series_ten_eighteen = sf.SeriesHE.from_dict(_start_end_ten_eighteen)

_start_end_mult_act_t_e = {"1": (datetime(2021, 1, 1, 10, 0),
                                 datetime(2021, 1, 2, 15, 0))}
start_end_series_mult_act_t_e = sf.SeriesHE.from_dict(_start_end_mult_act_t_e)


_start_end_mixed_activity = {"1": (datetime(2021, 1, 1, 10, 0),
                                   datetime(2021, 1, 1, 18, 0))}
start_end_series_mixed_activity = sf.SeriesHE.from_dict(_start_end_mixed_activity)

_start_end_mixed_case = {"1": (datetime(2021, 1, 1, 10, 0),
                               datetime(2021, 1, 1, 11, 0)),
                         "2": (datetime(2021, 1, 1, 10, 0),
                               datetime(2021, 1, 1, 18, 0))}
start_end_series_mixed_case = sf.SeriesHE.from_dict(_start_end_mixed_case)

basic_mock_gt = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1"],
    "concept:name": ["TestAct", "TestAct", "TestAct", "TestAct"],
    "lifecycle:transition": ["start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2023, 12, 13, 10, 0, 0), datetime(2023, 12, 13, 10, 0, 5),
                          datetime(2023, 12, 13, 10, 0, 8), datetime(2023, 12, 13, 10, 0, 9)],
})

basic_mock_det = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1"],
    "concept:name": ["TestAct", "TestAct", "TestAct", "TestAct"],
    "lifecycle:transition": ["start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2023, 12, 13, 10, 0, 3), datetime(2023, 12, 13, 10, 0, 7),
                          datetime(2023, 12, 13, 10, 0, 9), datetime(2023, 12, 13, 10, 0, 10)],
})

start_end_basic = {"1": (datetime(2023, 12, 13, 10, 0, 0),
                            datetime(2023, 12, 13, 10, 0, 10))}
start_end_series_basic = sf.SeriesHE.from_dict(start_end_basic)
start_end_series_basic_only_det = sf.SeriesHE.from_dict({"1": (datetime(2023, 12, 13, 10, 0, 3),
                                                                datetime(2023, 12, 13, 10, 0, 10))})


basic_mock_gt_1 = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1"],
    "concept:name": ["TestAct", "TestAct"],
    "lifecycle:transition": ["start", "complete"],
    "time:timestamp": [datetime(2023, 12, 13, 10, 0, 0), datetime(2023, 12, 13, 10, 0, 5)],
})

basic_mock_det_1 = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1"],
    "concept:name": ["TestAct", "TestAct"],
    "lifecycle:transition": ["start", "complete"],
    "time:timestamp": [datetime(2023, 12, 13, 10, 0, 5), datetime(2023, 12, 13, 10, 0, 10)],
})

start_end_basic_1 = {"1": (datetime(2023, 12, 13, 10, 0, 0),
                            datetime(2023, 12, 13, 10, 0, 10))}
start_end_series_basic_1 = sf.SeriesHE.from_dict(start_end_basic_1)
start_end_series_basic_1_only_det = sf.SeriesHE.from_dict({"1": (datetime(2023, 12, 13, 10, 0, 5),
                                                                datetime(2023, 12, 13, 10, 0, 10))})
start_end_series_basic_1_only_gt = sf.SeriesHE.from_dict({"1": (datetime(2023, 12, 13, 10, 0, 0),
                                                                datetime(2023, 12, 13, 10, 0, 5))})

basic_mock_gt_2 = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1"],
    "concept:name": ["TestAct", "TestAct", "TestAct", "TestAct"],
    "lifecycle:transition": ["start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2023, 12, 13, 10, 0, 8), datetime(2023, 12, 13, 10, 0, 9),
                          datetime(2023, 12, 13, 10, 0, 0), datetime(2023, 12, 13, 10, 0, 5)],
})

basic_mock_det_2 = sf.FrameHE.from_dict({
    "case:concept:name": ["1", "1", "1", "1"],
    "concept:name": ["TestAct", "TestAct", "TestAct", "TestAct"],
    "lifecycle:transition": ["start", "complete", "start", "complete"],
    "time:timestamp": [datetime(2023, 12, 13, 10, 0, 9), datetime(2023, 12, 13, 10, 0, 10),
                          datetime(2023, 12, 13, 10, 0, 3), datetime(2023, 12, 13, 10, 0, 7)],
})

start_end_basic_2 = {"1": (datetime(2023, 12, 13, 10, 0, 0),
                            datetime(2023, 12, 13, 10, 0, 10))}
start_end_series_basic_2 = sf.SeriesHE.from_dict(start_end_basic_2)
