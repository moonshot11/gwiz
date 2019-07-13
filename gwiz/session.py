# session.py

import json
from abc import ABC, abstractmethod

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

    def _get(self, url, base=None, params=None):
        """Submit a GET request, and return the JSON response"""
        result = []
        base = base or self._base
        params = params.copy() if params else dict()

        # Initialize pagination
        params['per_page'] = 20
        params['page'] = 1

        while True:
            resp = self._session.get(base + url, params=params)
            result +=  resp.json()
            if "next" in resp.links:
                params['page'] += 1
            else:
                break

        return result

    @abstractmethod
    def get_rate_limit(self):
        pass

    @property
    @abstractmethod
    def API_ROOT(self):
        pass

    @abstractmethod
    def __init__(self, user, proj):
        pass

    @abstractmethod
    def _get_labels(self):
        pass

    @abstractmethod
    def _get_issues(self):
        pass

    @abstractmethod
    def _get_comments(self):
        pass

    @abstractmethod
    def _apply_label(self, label):
        pass

    @abstractmethod
    def _apply_issue(self, issue):
        pass

    @abstractmethod
    def _delete_all_labels(self):
        pass

    @abstractmethod
    def _delete_all_issues(self):
        pass

    @abstractmethod
    def _format_data(self, data):
        """Dict -> format accepted by service"""
        pass
