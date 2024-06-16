=====
Usage
=====

To use AquDeM in a project:

.. code-block:: python

    import aqudem

    aqu_context = aqudem.Context("ground_truth_log.xes", "detected_log.xes")

    aqu_context.activity_names # get all activity names present in log
    aqu_context.case_ids # get all case IDs present in log

    aqu_context.cross_correlation() # aggregate over all cases and activites
    aqu_context.event_analysis(activity_name="Pack", case_id="1") # filter on case and activity
    aqu_context.two_set(activity_name="Pack") # filter on activity, aggregate over cases

