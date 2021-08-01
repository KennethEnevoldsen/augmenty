"""Utility functions for the package."""

import thinc
import catalogue

class registry(thinc.registry):
    keyboards = catalogue.create("augmenty", "keyboards", entry_points=True)

