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
        """Get issues from Gitlab project"""
        params = {"sort" : "asc"}
        data = self._session.get(self._base + "/issues", params=params).json()
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
        """Upload a label to Gitlab"""
        data = {
            "name" : label.title,
            "description" : label.desc,
            "color" : "#{}".format(label.color)
        }
        resp = self._session.post(
            self._base + "/labels", data=self._format_data(data))
        log.resp(resp.text)

    def _apply_issue(self, issue):
        """Upload an issue to Gitlab"""
        data = {
            "title" : issue._title,
            "description" : issue._desc,
            "labels" : issue._labels
        }
        state = issue._state
        log.info("Applying issue")
        resp = self._session.post(
            self._base + "/issues", data=self._format_data(data))
        log.resp(resp.text)
        iid = resp.json()['iid']
        if state == "closed":
            log.info("Updating state")
            resp = self._session.put(
                self._base + "/issues/{}".format(iid),
                data=self._format_data({"state_event" : "close"}))
            log.resp(resp.text)
        log.info("Done")

    def _delete_all_labels(self):
        """Delete all labels in a Github project"""
        data = self._session.get(self._base + "/labels").json()
        if not data:
            log.info("No labels found!")
            return
        for item in data:
            info = {"name" : item['name']}
            resp = self._session.delete(
                self._base + "/labels",
                data=self._format_data(info))
            if resp.status_code == 204:
                log.resp("204: Deleted label " + item['name'])
            else:
                log.resp("{}: {}".format(resp.status_code, resp.text))

    def _delete_all_issues(self):
        """Delete all issues in a Gitlab project"""
        data = self._session.get(self._base + "/issues").json()
        if not data:
            log.info("No issues found!")
            return
        for item in data:
            resp = self._session.delete(
                self._base + "/issues/{}".format(item['iid']))
            if resp.status_code == 204:
                log.resp("204: Deleted issue " + item['title'])
            else:
                log.resp("{}: {}".format(resp.status_code, resp.text))

    def _format_data(self, data):
        """Dict -> format accepted by service"""
        return data
