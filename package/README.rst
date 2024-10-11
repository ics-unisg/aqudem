======
AquDeM
======


.. image:: https://img.shields.io/pypi/v/aqudem.svg
        :target: https://pypi.python.org/pypi/aqudem

.. image:: https://readthedocs.org/projects/aqudem/badge/?version=latest
        :target: https://aqudem.readthedocs.io
        :alt: Documentation Status



Activity and Sequence Detection Evaluation Metrics: A Comprehensive Tool for Event Log Comparison.

* Documentation: https://aqudem.readthedocs.io

Installation
------------
.. code-block:: bash

    pip install aqudem

Usage
-----
.. code-block:: python

    import aqudem

    aqu_context = aqudem.Context("ground_truth_log.xes", "detected_log.xes")

    aqu_context.activity_names # get all activity names present in log
    aqu_context.case_ids # get all case IDs present in log

    aqu_context.cross_correlation() # aggregate over all cases and activites
    aqu_context.event_analysis(activity_name="Pack", case_id="1") # filter on case and activity
    ts = aqu_context.two_set(activity_name="Pack") # filter on activity, aggregate over cases
    ts_f1_score = ts.f1 # get the F1 score of the Two Set metric

For a more detailed description of the available methods, please refer to the rest of the documentation.

Preface
--------

* Metrics to evaluate activity detection results
* Input: two XES files, one with the ground truth and one with the detection results
* Output: a set of metrics to evaluate the detection results
* Prerequisites for the input files: the XES files must...

  * ... have a ``sampling_freq`` in Hz associated with each case (only detected file), and each case must have the same sampling frequency
  * ... have a ``concept:name`` attribute for each case (case ID), with a matching case ID in both files (ground truth and detected)
  * ... have a ``time:timestamp`` attribute for each event
  * ... have an ``concept:name`` attribute for each event (activity name)
  * ... have a ``lifecycle:transition`` attribute for each event
  * ... each ``start`` event must have a corresponding ``complete`` event; and only these two types of events are relevant for the analysis currently; activity executions with a duration of exactly zero are removed


An ACTIVITY_METRIC is a metric that is calculated for each activity type
in each case separately.
Available ACTIVITY_METRICs are:

* Cross-Correlation
* Event Analysis by `Ward et al. (2011)`_
* Two Set Metrics by `Ward et al. (2011)`_

A SEQUENCE_METRIC is a metric that is calculated for each
case separately.
Available SEQUENCE_METRICs are:

* Damerau-Levenshtein Distance
* Levenshtein Distance


All metrics are also available in appropriately normalized versions.
For requests that span multiple cases, the results are aggregated. The default and only aggregation method is currently the mean.
For more detailed definitions of the metrics, please refer to the documentation.



.. _`Ward et al. (2011)`: https://doi.org/10.1145/1889681.1889687
