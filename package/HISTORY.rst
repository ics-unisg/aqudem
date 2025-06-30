=======
History
=======

0.3.0 (2025-06-29)
------------------

Make it more clear that EA and TS derived metrics/rates are micro-averaged:

In order to clarify the nature of the rates and metrics such as F1 of the event analysis and two set metrics we decided to give sums of event and frame classification totals. Derived metrics are then more clearly understood to be micro-averaged. The average over all case-activity case-pairs was prone to misinterpretation. Furthermore we improved the documentation of the code to reflect this aspect.

More details on micro-averaging: https://doi.org/10.1016/j.ipm.2009.03.002

0.2.1 (2025-05-01)
------------------

Resolved some dependency issues (by updating all requirements to newest version).

0.2.0 (2024-10-11)
------------------

Added additional properties for the EventAnalysis and TwoSet classes, for a better overview of the performance of methods.
The main additions are:

* The TwoSet class now offers the properties precision, recall, f1, and balanced_accuracy.
* The EventAnalysis class now offers the properties precision, recall, and f1 (balanced_accuracy does not make sense here, since there is no notion of true negative events).

0.1.1 (2024-08-14)
------------------

* Added additional validations and checks for the input logs, with helpful tips in errors in case of non-compliance.
* Minor bug fixes.

0.1.0 (2024-06-19)
------------------

* First release on PyPI.
