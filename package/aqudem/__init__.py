"""Top-level package for AquDeM."""
from .aqudem import Context
from .event_analysis_helper import EventAnalysis
from .two_set_helper import TwoSet
from .utils import (XESMissingTraceNameAttribute,XESMissingSamplingFreqError,
                    XESMissingTimestamp, XESMissingActivityName, XESMissingActivityInstance,
                    XESIncorrectLifecycleTransitionError)

__author__ = """ICS, Universität St. Gallen"""
__email__ = 'aaron.kurz@unisg.ch'
__version__ = '0.1.0'

__all__ = ["Context",
           "EventAnalysis",
           "TwoSet",
           "XESMissingTraceNameAttribute",
           "XESMissingSamplingFreqError",
           "XESMissingTimestamp",
           "XESMissingActivityName",
           "XESMissingActivityInstance",
           "XESIncorrectLifecycleTransitionError"]
