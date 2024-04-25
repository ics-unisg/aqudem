======
AquDeM
======


.. image:: https://img.shields.io/pypi/v/aqudem.svg
        :target: https://pypi.python.org/pypi/aqudem

.. image:: https://readthedocs.org/projects/aqudem/badge/?version=latest
        :target: https://aqudem.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



Activity and Sequence Detection Performance Measures: A package to evaluate activity detection results, including the sequence of events given multiple activity types.

* Documentation: https://aqudem.readthedocs.io. (TODO: not yet active)

Installation
------------
.. code-block:: bash

    pip install .

Usage
-----
.. code-block:: python

    import aqudem

    aqu_context = aqudem.Context("ground_truth.xes",
                                 "detected.xes")

    aqu_context.activity_names
    aqu_context.case_ids
    aqu_context.cross_correlation()
    aqu_context.event_analysis(activity_name="Store Workpiece in HBW", case_id="case1")
    aqu_context.two_set(activity_name="Store Workpiece in HBW")
    aqu_context.levenshtein_distance()


For a more detailed description of the available methods, please refer to the rest of the documentation.

Preface
--------

* Measurements and metrics to evaluate activity detection results
* Input: two XES files, one with the ground truth and one with the detection results
* Output: a set of metrics to evaluate the detection results
* Prerequisites for the input files: the XES files must...

  * ... have a ``sampling_freq`` in Hz associated with each case
  * ... have a ``concept:name`` attribute for each case
  * ... have a ``time:timestamp`` attribute for each event
  * ... have an ``concept:name`` attribute for each event (activity name)
  * ... have a ``lifecycle:transition`` attribute for each event
  * ... each ``start`` event must have a corresponding ``complete`` event; and only these two types of events are relevant for the analysis currently


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

For requests that span multiple cases, the results are aggregated. The default and only aggregation method is currently averaging.

Classifications are specified in the docstrings of the public
metric methods of aqudem.Context.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Ward et al. (2011)`: https://doi.org/10.1145/1889681.1889687
