# session.py

import json
from abc import ABC, abstractmethod as absmth

# TODO: Make this class abstract once interface is defined
class Session():
    """A generic web session"""

    def write_json(self, filename, only=None):
        """Write labels to filename"""
        data = dict()
        if only is None or only == "labels":
            labels = [lbl.as_dict for lbl in self._get_labels()]
            data["labels"] = labels
        if only is None or only == "issues":
            pass
        with open(filename, "w") as fout:
            json.dump(data, fout)
