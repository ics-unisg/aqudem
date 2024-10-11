=======
History
=======

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
