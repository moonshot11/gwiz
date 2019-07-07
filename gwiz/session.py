# session.py

import json
from abc import ABC, abstractmethod as absmth

# TODO: Make this class abstract once interface is defined
class Session():
    """A generic web session"""

    def write_labels(self, filename):
        """Write labels to filename"""
        labels = self._get_labels()
        data = [lbl.as_dict for lbl in labels]
        with open(filename, "w") as fout:
            json.dump(data, fout)
