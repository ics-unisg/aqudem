"""AquDeM visual interface."""
import json
import os
from tempfile import NamedTemporaryFile
from typing import List
import pandas as pd
import streamlit as st
import altair as alt
import aqudem

st.set_page_config(
    page_title="AquDeM",
    page_icon="📊",
)
if "active_analysis" not in st.session_state:
    st.session_state.active_analysis = False

if "context" not in st.session_state:
    st.session_state.context = None


# --------- HELPER FUNCTIONS ---------

def get_activity_choices():
    """Get the activity choices for the metrics."""
    all_activities: List[str] = list(
        set(st.session_state.context.activity_names["ground_truth"]
            + st.session_state.context.activity_names["detected"]))
    return st.multiselect(
        "Which activities are you interested in?",
        options=all_activities,
        help="Leave empty to average over all activities")


def get_case_choices():
    """Get the case choices for the metrics."""
    all_cases: List[str] = list(
        set(st.session_state.context.case_ids["ground_truth"]
            + st.session_state.context.case_ids["detected"]))
    return st.multiselect(
        "Which cases are you interested in?",
        options=all_cases,
        help="Leave empty to average over all cases")


# --------- METRIC CONTENT FUNCTIONS ---------

def get_cross_correlation_content():
    """Get the content for the cross-correlation metric."""
    case_choices = get_case_choices()
    activity_choices = get_activity_choices()
    metric_res_list = []
    for activity in activity_choices if len(activity_choices) > 0 else ["*"]:
        for case in case_choices if len(case_choices) > 0 else ["*"]:
            if metric_choice == "Cross-correlation":
                metric_res_list.append({
                    "activity": activity,
                    "case": case,
                    "cross-correlation": st.session_state.context.cross_correlation(activity, case)[
                        0]
                })
    metric_res = pd.DataFrame(metric_res_list)
    if not metric_res.empty:
        st.dataframe(metric_res, use_container_width=True)
        metric_res['activity-case'] = metric_res['activity'].astype(str) + '-' + metric_res[
            'case'].astype(str)
        chart = alt.Chart(metric_res).mark_bar().encode(
            y=alt.Y("cross-correlation:Q", title="Cross-correlation"),
            x=alt.X("activity-case:N", title="Activity-Case")
        ).properties(
            height=400
        )
        st.altair_chart(chart, use_container_width=True)


def get_damerau_levenshtein_norm_content():
    """Get the content for the normed Damerau-Levenshtein metric."""
    case_choices_dl = get_case_choices()
    metric_res_list_dl = []
    for case in case_choices_dl if len(case_choices_dl) > 0 else ["*"]:
        metric_res_list_dl.append({
            "case": case,
            "damerau-levenshtein": st.session_state.context.damerau_levenshtein_distance(case)[1]
        })
    metric_res_dl = pd.DataFrame(metric_res_list_dl)
    if not metric_res_dl.empty:
        st.dataframe(metric_res_dl, use_container_width=True)
        chart_dl = alt.Chart(metric_res_dl).mark_bar().encode(
            y=alt.Y("damerau-levenshtein:Q", title="Damerau-Levenshtein norm"),
            x=alt.X("case:N", title="Case")
        ).properties(
            height=400
        )
        st.altair_chart(chart_dl, use_container_width=True)


def get_damerau_levenshtein_content():
    """Get the content for the Damerau-Levenshtein metric."""
    case_choices_dl = get_case_choices()
    metric_res_list_dl = []
    for case in case_choices_dl if len(case_choices_dl) > 0 else ["*"]:
        metric_res_list_dl.append({
            "case": case,
            "damerau-levenshtein": st.session_state.context.damerau_levenshtein_distance(case)[0]
        })
    metric_res_dl = pd.DataFrame(metric_res_list_dl)
    if not metric_res_dl.empty:
        st.dataframe(metric_res_dl, use_container_width=True)
        chart_dl = alt.Chart(metric_res_dl).mark_bar().encode(
            y=alt.Y("damerau-levenshtein:Q", title="Damerau-Levenshtein distance"),
            x=alt.X("case:N", title="Case")
        ).properties(
            height=400
        )
        st.altair_chart(chart_dl, use_container_width=True)


def get_levenshtein_norm_content():
    """Get the content for the normed Levenshtein metric."""
    case_choices_l = get_case_choices()
    metric_res_list_l = []
    for case in case_choices_l if len(case_choices_l) > 0 else ["*"]:
        metric_res_list_l.append({
            "case": case,
            "levenshtein": st.session_state.context.levenshtein_distance(case)[1]
        })
    metric_res_l = pd.DataFrame(metric_res_list_l)
    if not metric_res_l.empty:
        st.dataframe(metric_res_l, use_container_width=True)
        chart_l = alt.Chart(metric_res_l).mark_bar().encode(
            y=alt.Y("levenshtein:Q", title="Levenshtein norm"),
            x=alt.X("case:N", title="Case")
        ).properties(
            height=400
        )
        st.altair_chart(chart_l, use_container_width=True)


def get_levenshtein_content():
    """Get the content for the Levenshtein metric."""
    case_choices_l = get_case_choices()
    metric_res_list_l = []
    for case in case_choices_l if len(case_choices_l) > 0 else ["*"]:
        metric_res_list_l.append({
            "case": case,
            "levenshtein": st.session_state.context.levenshtein_distance(case)[0]
        })
    metric_res_l = pd.DataFrame(metric_res_list_l)
    if not metric_res_l.empty:
        st.dataframe(metric_res_l, use_container_width=True)
        chart_l = alt.Chart(metric_res_l).mark_bar().encode(
            y=alt.Y("levenshtein:Q", title="Levenshtein distance"),
            x=alt.X("case:N", title="Case")
        ).properties(
            height=400
        )
        st.altair_chart(chart_l, use_container_width=True)


def get_2set_metrics_content():
    """Get the content for the 2SET metrics."""
    case_choices_2set = get_case_choices()
    activity_choices_2set = get_activity_choices()
    metric_res_list_2set = []
    for activity in activity_choices_2set if len(activity_choices_2set) > 0 else ["*"]:
        for case in case_choices_2set if len(case_choices_2set) > 0 else ["*"]:
            metric_res_list_2set.append({
                "activity": activity,
                "case": case,
                "2SET": st.session_state.context.two_set(activity, case)
            })
    metric_res_2set = pd.DataFrame(metric_res_list_2set)
    if not metric_res_2set.empty:
        metric_res_2set["tp"] = metric_res_2set["2SET"].apply(lambda x: x.tp)
        metric_res_2set["tn"] = metric_res_2set["2SET"].apply(lambda x: x.tn)
        metric_res_2set["d"] = metric_res_2set["2SET"].apply(lambda x: x.d)
        metric_res_2set["f"] = metric_res_2set["2SET"].apply(lambda x: x.f)
        metric_res_2set["ua"] = metric_res_2set["2SET"].apply(lambda x: x.ua)
        metric_res_2set["uo"] = metric_res_2set["2SET"].apply(lambda x: x.uo)
        metric_res_2set["i"] = metric_res_2set["2SET"].apply(lambda x: x.i)
        metric_res_2set["m"] = metric_res_2set["2SET"].apply(lambda x: x.m)
        metric_res_2set["oa"] = metric_res_2set["2SET"].apply(lambda x: x.oa)
        metric_res_2set["oo"] = metric_res_2set["2SET"].apply(lambda x: x.oo)
        metric_res_2set.drop(columns=["2SET"], inplace=True)
        st.dataframe(metric_res_2set, use_container_width=True)
        with st.expander("Explanation of acronyms"):
            st.markdown(
                "These explain what 'happened to' the frames that are "
                "positive in the ground truth in the detected log:\n"
                "Number of...:\n"
                "- tp: True positives\n"
                "- d: Deletions\n"
                "- f: Fragmentations\n"
                "- ua: Underfills $\\alpha$\n"
                "- uo: Underfills $\\omega$\n\n"
                "These explain what 'happened to' the frames that are "
                "negative in the ground truth in the detected log:\n"
                "Number of...:\n"
                "- tn: True negatives\n"
                "- i: Insertions\n"
                "- m: Mergings\n"
                "- oa: Overfills $\\alpha$\n"
                "- oo: Overfills $\\omega$\n\n"
                "For more details, please see the [paper by Ward et al "
                "(2011)](https://doi.org/10.1145/1889681.1889687).")
        metric_res_2set['activity-case'] = metric_res_2set['activity'].astype(str) + '-' + \
                                           metric_res_2set[
                                               'case'].astype(str)
        metric_choices = ["tp", "tn", "d", "f", "ua", "uo", "i", "m", "oa", "oo"]
        metric_choice_2set = st.selectbox("Which 2SET metric do you want to visualize?",
                                          options=metric_choices)
        chart_2set = alt.Chart(metric_res_2set).mark_bar().encode(
            y=alt.Y(f"{metric_choice_2set}:Q", title=metric_choice_2set),
            x=alt.X("activity-case:N", title="Activity-Case")
        ).properties(
            height=400
        )
        st.altair_chart(chart_2set, use_container_width=True)


def get_2set_rates_content():
    """Get the content for the 2SET rates."""
    case_choices_2set = get_case_choices()
    activity_choices_2set = get_activity_choices()
    metric_res_list_2set = []
    for activity in activity_choices_2set if len(activity_choices_2set) > 0 else ["*"]:
        for case in case_choices_2set if len(case_choices_2set) > 0 else ["*"]:
            metric_res_list_2set.append({
                "activity": activity,
                "case": case,
                "2SET": st.session_state.context.two_set(activity, case)
            })
    metric_res_2set = pd.DataFrame(metric_res_list_2set)
    if not metric_res_2set.empty:
        metric_res_2set["tpr"] = metric_res_2set["2SET"].apply(lambda x: x.tpr)
        metric_res_2set["tnr"] = metric_res_2set["2SET"].apply(lambda x: x.tnr)
        metric_res_2set["dr"] = metric_res_2set["2SET"].apply(lambda x: x.dr)
        metric_res_2set["fr"] = metric_res_2set["2SET"].apply(lambda x: x.fr)
        metric_res_2set["uar"] = metric_res_2set["2SET"].apply(lambda x: x.uar)
        metric_res_2set["uor"] = metric_res_2set["2SET"].apply(lambda x: x.uor)
        metric_res_2set["ir"] = metric_res_2set["2SET"].apply(lambda x: x.ir)
        metric_res_2set["mr"] = metric_res_2set["2SET"].apply(lambda x: x.mr)
        metric_res_2set["oar"] = metric_res_2set["2SET"].apply(lambda x: x.oar)
        metric_res_2set["oor"] = metric_res_2set["2SET"].apply(lambda x: x.oor)
        metric_res_2set.drop(columns=["2SET"], inplace=True)
        st.dataframe(metric_res_2set, use_container_width=True)
        with st.expander("Explanation of acronyms"):
            st.markdown(
                "These explain what 'happened to' the frames that are positive "
                "in the ground truth in the detected log:\n"
                "Rate of...:\n"
                "- tpr: True positives\n"
                "- dr: Deletions\n"
                "- fr: Fragmentations\n"
                "- uar: Underfills $\\alpha$\n"
                "- uor: Underfills $\\omega$\n\n"
                "These explain what 'happened to' the frames that are "
                "negative in the ground truth in the detected log:\n"
                "Rate of...:\n"
                "- tnr: True negatives\n"
                "- ir: Insertions\n"
                "- mr: Mergings\n"
                "- oar: Overfills $\\alpha$\n"
                "- oor: Overfills $\\omega$\n\n"
                "For more details, please see the [paper by Ward et al "
                "(2011)](https://doi.org/10.1145/1889681.1889687).")
        pie_chart_dict_p = {
            "category": [],
            "value": []
        }
        for metric_p in ["tpr", "dr", "fr", "uar", "uor"]:
            pie_chart_dict_p["category"].append(metric_p)
            pie_chart_dict_p["value"].append(metric_res_2set[metric_p].mean())
        pie_chart_df = pd.DataFrame(pie_chart_dict_p)
        chart_p = alt.Chart(pie_chart_df).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="category", type="nominal"),
        )
        st.write(
            "How the positive ground truth frames were classified "
            "(averaged over your selected combinations/rows from above):")
        st.altair_chart(chart_p, use_container_width=True)
        pie_chart_dict_n = {
            "category": [],
            "value": []
        }
        for metric_n in ["tnr", "ir", "mr", "oar", "oor"]:
            pie_chart_dict_n["category"].append(metric_n)
            pie_chart_dict_n["value"].append(metric_res_2set[metric_n].mean())
        pie_chart_df = pd.DataFrame(pie_chart_dict_n)
        chart_n = alt.Chart(pie_chart_df).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="category", type="nominal"),
        )
        st.write(
            "How the negative ground truth frames were classified "
            "(averaged over your selected combinations/rows from above):")
        st.altair_chart(chart_n, use_container_width=True)


def get_event_analysis_metrics_content():
    """Get the content for the event analysis metrics."""
    case_choices = get_case_choices()
    activity_choices = get_activity_choices()
    metric_res_list = []
    for activity in activity_choices if len(activity_choices) > 0 else ["*"]:
        for case in case_choices if len(case_choices) > 0 else ["*"]:
            if metric_choice == "Event analysis":
                metric_res_list.append({
                    "activity": activity,
                    "case": case,
                    "event-analysis": st.session_state.context.event_analysis(activity, case)
                })
    metric_res = pd.DataFrame(metric_res_list)
    if not metric_res.empty:
        metric_res["d"] = metric_res["event-analysis"].apply(lambda x: x.d)
        metric_res["f"] = metric_res["event-analysis"].apply(lambda x: x.f)
        metric_res["fm"] = metric_res["event-analysis"].apply(lambda x: x.fm)
        metric_res["m"] = metric_res["event-analysis"].apply(lambda x: x.m)
        metric_res["c"] = metric_res["event-analysis"].apply(lambda x: x.c)
        metric_res["md"] = metric_res["event-analysis"].apply(lambda x: x.md)
        metric_res["fmd"] = metric_res["event-analysis"].apply(lambda x: x.fmd)
        metric_res["fd"] = metric_res["event-analysis"].apply(lambda x: x.fd)
        metric_res["id"] = metric_res["event-analysis"].apply(lambda x: x.id)
        metric_res.drop(columns=["event-analysis"], inplace=True)
        st.dataframe(metric_res, use_container_width=True)
        with st.expander("Explanation of acronyms"):
            st.markdown("These explain what 'happened to' the events from the ground truth :\n"
                        "Number of...:\n"
                        "- d: Deletions\n"
                        "- f: Fragmentations\n"
                        "- fm: Fragmentatations and mergings\n"
                        "- m: Mergings\n"
                        "- c: Correct detections\n"
                        "These explain/classify the events that have been detected:\n"
                        "Number of...:\n"
                        "- md: Mergings\n"
                        "- fmd: Fragmentations and mergings\n"
                        "- fd: Fragmentations\n"
                        "- id: Insertions\n\n"
                        "For more details, please see the "
                        "[paper by Ward et al (2011)](https://doi.org/10.1145/1889681.1889687).")
        metric_res['activity-case'] = metric_res['activity'].astype(str) + '-' + metric_res[
            'case'].astype(str)
        metric_choices = ["d", "f", "fm", "m", "c", "md", "fmd", "fd", "id"]
        metric_choice_event = st.selectbox("Which event analysis metric do you want to visualize?",
                                           options=metric_choices)
        chart_event = alt.Chart(metric_res).mark_bar().encode(
            y=alt.Y(f"{metric_choice_event}:Q", title=metric_choice_event),
            x=alt.X("activity-case:N", title="Activity-Case")
        ).properties(
            height=400
        )
        st.altair_chart(chart_event, use_container_width=True)


def get_event_analysis_rates_content():
    """Get the content for the event analysis rates."""
    case_choices = get_case_choices()
    activity_choices = get_activity_choices()
    metric_res_list = []
    for activity in activity_choices if len(activity_choices) > 0 else ["*"]:
        for case in case_choices if len(case_choices) > 0 else ["*"]:
            if metric_choice == "Event analysis rates":
                metric_res_list.append({
                    "activity": activity,
                    "case": case,
                    "event-analysis": st.session_state.context.event_analysis(activity, case)
                })
    metric_res = pd.DataFrame(metric_res_list)
    if not metric_res.empty:
        metric_res["dr"] = metric_res["event-analysis"].apply(lambda x: x.dr)
        metric_res["fr"] = metric_res["event-analysis"].apply(lambda x: x.fr)
        metric_res["fmr"] = metric_res["event-analysis"].apply(lambda x: x.fmr)
        metric_res["mr"] = metric_res["event-analysis"].apply(lambda x: x.mr)
        metric_res["cr_gt"] = metric_res["event-analysis"].apply(lambda x: x.cr_gt)
        metric_res["mdr"] = metric_res["event-analysis"].apply(lambda x: x.mdr)
        metric_res["fmdr"] = metric_res["event-analysis"].apply(lambda x: x.fmdr)
        metric_res["fdr"] = metric_res["event-analysis"].apply(lambda x: x.fdr)
        metric_res["idr"] = metric_res["event-analysis"].apply(lambda x: x.idr)
        metric_res["cr_det"] = metric_res["event-analysis"].apply(lambda x: x.cr_det)
        metric_res.drop(columns=["event-analysis"], inplace=True)
        st.dataframe(metric_res, use_container_width=True)
        with st.expander("Explanation of acronyms"):
            st.markdown("These explain what 'happened to' the events from the ground truth :\n"
                        "Rate of...:\n"
                        "- dr: Deletions\n"
                        "- fr: Fragmentations\n"
                        "- fmr: Fragmentatations and mergings\n"
                        "- mr: Mergings\n"
                        "- cr_gt: Correct detections\n"
                        "These explain/classify the events that have been detected:\n"
                        "Rate of...:\n"
                        "- mdr: Mergings\n"
                        "- fmdr: Fragmentations and mergings\n"
                        "- fdr: Fragmentations\n"
                        "- idr: Insertions\n"
                        "- cr_det: Correct detections\n\n"
                        "For more details, please see the "
                        "[paper by Ward et al (2011)](https://doi.org/10.1145/1889681.1889687).")
        pie_chart_dict_p = {
            "category": [],
            "value": []
        }
        for metric_p in ["dr", "fr", "fmr", "mr", "cr_gt"]:
            pie_chart_dict_p["category"].append(metric_p)
            pie_chart_dict_p["value"].append(metric_res[metric_p].mean())
        pie_chart_df = pd.DataFrame(pie_chart_dict_p)
        chart_p = alt.Chart(pie_chart_df).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="category", type="nominal"),
        )
        st.write(
            "How the positive ground truth events were classified "
            "(averaged over your selected combinations/rows from above):")
        st.altair_chart(chart_p, use_container_width=True)
        pie_chart_dict_n = {
            "category": [],
            "value": []
        }
        for metric_n in ["mdr", "fmdr", "fdr", "idr", "cr_det"]:
            pie_chart_dict_n["category"].append(metric_n)
            pie_chart_dict_n["value"].append(metric_res[metric_n].mean())
        pie_chart_df = pd.DataFrame(pie_chart_dict_n)
        chart_n = alt.Chart(pie_chart_df).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="category", type="nominal"),
        )
        st.write(
            "How the negative ground truth events were classified "
            "(averaged over your selected combinations/rows from above):")
        st.altair_chart(chart_n, use_container_width=True)


# --------- MAIN FLOW ---------

st.header("AquDeM 📊")
if not st.session_state.active_analysis and st.session_state.context is None:
    st.write("Please upload the ground truth and detected logs to start the analysis.")
    gt_upload = st.file_uploader("Upload ground truth log",
                                 key="gt_uploader",
                                 type=["xes"])
    det_upload = st.file_uploader("Upload detected log",
                                  key="det_uploader",
                                  type=["xes"])
    if st.button("Start analysis"):
        if gt_upload is not None and det_upload is not None:
            st.session_state.active_analysis = True
            # temporarily store the uploaded files on disk
            with NamedTemporaryFile(delete=False) as gt_f:  # Create temporary file
                gt_f.write(gt_upload.getvalue())  # Save uploaded contents to file
            with NamedTemporaryFile(delete=False) as det_f:  # Create temporary file
                det_f.write(det_upload.getvalue())  # Save uploaded contents to file
            st.session_state.context = aqudem.Context(gt_f.name, det_f.name)
            # delete temporary file from filesystem
            os.remove(gt_f.name)
            os.remove(det_f.name)
            st.rerun()
        else:
            st.toast("Please upload both the ground truth "
                     "and detected logs to start the analysis.",
                     icon="⚠️")
elif st.session_state.active_analysis and st.session_state.context is not None:
    interactive_tab, download_tab, about_tab = st.tabs(["Interactive", "Download", "About"])
    with interactive_tab:
        metrics = ["Cross-correlation", "Damerau-Levenshtein", "Levenshtein",
                   "Damerau-Levenshtein normalized", "Levenshtein normalized",
                   "2SET metrics", "2SET rates", "Event analysis", "Event analysis rates"]
        metric_choice = st.selectbox("Which metric are you interested in?",
                                     options=metrics,
                                     help=("For more information on the metrics, please "
                                           "refer to [the metrics overview in "
                                           "the documentation](https://sdgs.un.org/goals)"))
        if metric_choice == "Cross-correlation":
            get_cross_correlation_content()
        elif metric_choice == "Damerau-Levenshtein":
            get_damerau_levenshtein_content()
        elif metric_choice == "Levenshtein":
            get_levenshtein_content()
        elif metric_choice == "Damerau-Levenshtein normalized":
            get_damerau_levenshtein_norm_content()
        elif metric_choice == "Levenshtein normalized":
            get_levenshtein_norm_content()
        elif metric_choice == "2SET metrics":
            get_2set_metrics_content()
        elif metric_choice == "2SET rates":
            get_2set_rates_content()
        elif metric_choice == "Event analysis":
            get_event_analysis_metrics_content()
        elif metric_choice == "Event analysis rates":
            get_event_analysis_rates_content()
    with download_tab:
        st.write("AquDeM offers the possibility to download the results of the analysis "
                 "of the overall log in "
                 "a structured format. This allows for aggregation and further analysis.")
        st.write("Please specify the tags you want to include in the download, to help"
                 " with the analysis.")
        download_tags_df = pd.DataFrame(columns=["Tag Name", "Tag Value"])
        edited_tags_df = st.data_editor(download_tags_df, num_rows="dynamic")
        tags_dict = edited_tags_df.set_index("Tag Name")["Tag Value"].to_dict()
        download_dict = {}
        download_dict["tags"] = tags_dict
        download_dict["cross-correlation"] = st.session_state.context.cross_correlation()[0]
        download_dict["two-set-correlation-shift"] = st.session_state.context.cross_correlation()[1]
        twoset_obj = st.session_state.context.two_set()
        dict_with_cached_properties_twoset = {}
        for attr_name in dir(twoset_obj):
            attr_value = getattr(twoset_obj, attr_name)
            if isinstance(attr_value, property):
                dict_with_cached_properties_twoset[attr_name] = attr_value.fget(twoset_obj)
        dict_with_cached_properties_twoset.update(twoset_obj.__dict__)
        download_dict["two-set"] = dict_with_cached_properties_twoset
        eventanalysis_obj = st.session_state.context.event_analysis()
        dict_with_cached_properties_eventanalysis = {}
        for attr_name in dir(eventanalysis_obj):
            attr_value = getattr(eventanalysis_obj, attr_name)
            if isinstance(attr_value, property):
                dict_with_cached_properties_eventanalysis[attr_name] = attr_value.fget(
                    eventanalysis_obj)
        dict_with_cached_properties_eventanalysis.update(eventanalysis_obj.__dict__)
        download_dict["event-analysis"] = dict_with_cached_properties_eventanalysis
        download_dict["damerau-levenshtein"] = \
            st.session_state.context.damerau_levenshtein_distance()[0]
        download_dict["damerau-levenshtein-norm"] = \
            st.session_state.context.damerau_levenshtein_distance()[1]
        download_dict["levenshtein"] = st.session_state.context.levenshtein_distance()[0]
        download_dict["levenshtein-norm"] = st.session_state.context.levenshtein_distance()[1]
        st.download_button(label="Download with tags",
                           data=json.dumps(download_dict, indent=4, separators=(',', ': ')),
                           file_name="AquDeM_results.json")
    with about_tab:
        st.write("Interactive, visual evaluation of activity detection results.")
        st.write("For more information, please refer to the "
                 "[documentation](https://sdgs.un.org/goals) "
                 "or [GitHub repository](https://github.com/ics-unisg/aqudem).")
