# session.py

import json
import time
from abc import ABC, abstractmethod

from gwiz import log
from gwiz.issue import Issue, Comment
from gwiz.label import Label

# TODO: Make this class abstract once interface is defined
class Session():
    """A generic web session"""

    # In seconds, after each post request
    DELAY = 1

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
            # Apply labels
            labels = Label.json_to_labels(data["labels"])
            for i, label in enumerate(labels):
                log.info('Posting label ({}/{}) "{}"...'.format(
                    i+1, len(labels), label.title), end='')
                self._apply_label(label)
                print("done!")

        if only is None or only == "issues":
            # Apply issues
            issues = Issue.json_to_issues(data["issues"])
            for i, issue in enumerate(issues):
                log.info('Posting issue ({}/{}) "{}"...'.format(
                    i+1, len(issues), issue._title), end='')
                iid = self._apply_issue(issue)
                print("done!")

                # Apply comments
                for j, comment in enumerate(issue._comments):
                    log.info('  Posting comment ({}/{}) to issue #{}...'.format(
                        j+1, len(issue._comments), iid), end='')
                    self._apply_comment(iid, comment)
                    print("done!")


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

    def _post(self, *args, **kwargs):
        return self._update_wrapper(self._session.post, *args, **kwargs)

    def _patch(self, *args, **kwargs):
        return self._update_wrapper(self._session.patch, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._update_wrapper(self._session.delete, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._update_wrapper(self._session.put, *args, **kwargs)

    def _update_wrapper(self, func, *args, **kwargs):
        """Delay for POST, PATCH, PUT, and DELETE"""
        time.sleep(self.DELAY)
        resp = func(*args, **kwargs)
        return resp

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
    def _apply_comment(self, iid, comment):
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
