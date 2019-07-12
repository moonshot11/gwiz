# gitlab.py

import json
import requests

from gwiz.issue import Issue, Comment
from gwiz.label import Label
from gwiz import log
from gwiz import session

class Gitlab(session.Session):
    """A web session for Gitlab"""

    def __init__(self, user, proj):
        """Initialize a Gitlab session"""
        auth_hdr = {"Private-Token" : input("Enter PA token: ")}
        self._session = requests.Session()
        self._session.headers.update(auth_hdr)
        self._base = "https://gitlab.com/api/v4/projects/{}".format(proj)

    def _get_labels(self):
        """Return labels"""
        data = self._session.get(self._base + "/labels").json()
        labels = []
        for lbl in data:
            labels.append(
                Label(lbl['name'], lbl['color'][1:],
                lbl.get("description") or "")
            )
        return labels

    def _get_issues(self):
        data = self._session.get(self._base + "/issues").json()
        issues = []
        for item in data:
            issue = Issue(item['title'], item['description'], item['labels'], item['state'])
            if item['user_notes_count'] > 0:
                issue._comments = self._get_comments(item['iid'])
            issues.append(issue)
        return issues

    def _get_comments(self, issue_id):
        data = self._session.get(self._base + "/issues/{}/notes".format(issue_id))
        data = data.json()
        comments = []
        for item in data:
            comments.append(
                Comment(item['author']['username'], item['body'])
            )
        return comments

    def _apply_label(self, label):
        pass

    def _apply_issue(self, issue):
        pass

    def _delete_all_labels(self):
        pass

    def _delete_all_issues(self):
        pass

    def _format_data(self, data):
        """Dict -> format accepted by service"""
        pass
