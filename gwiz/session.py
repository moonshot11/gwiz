# session.py

import json
from abc import ABC, abstractmethod as absmth

from gwiz.issue import Issue, Comment
from gwiz.label import Label

# TODO: Make this class abstract once interface is defined
class Session():
    """A generic web session"""

    def write_json(self, filename, only=None):
        """Write labels to filename"""
        data = dict()
        if only is None or only == "labels":
            labels = [lbl.as_dict() for lbl in self._get_labels()]
            data["labels"] = labels
        if only is None or only == "issues":
            issues = [iss.as_dict() for iss in self._get_issues()]
            data["issues"] = issues

        with open(filename, "w") as fout:
            json.dump(data, fout)

    def apply_json(self, filename, only=None):
        """Apply json data to web repo"""
        with open(filename, "r") as fin:
            data = json.load(fin)

        if only is None or only == "labels":
            for label in Label.json_to_labels(data["labels"]):
                self._apply_label(label)
        if only is None or only == "issues":
            for issue in Issue.json_to_issues(data["issues"]):
                self._apply_issue(issue)

    def delete_all(self, only):
        """Delete all labels"""
        if only is None or only == "labels":
            self._delete_all_labels()
        if only is None or only == "issues":
            self._delete_all_issues()
