# github.py

import json
import requests

from gwiz.issue import Issue, Comment
from gwiz.label import Label
from gwiz import log
from gwiz import session

class Github(session.Session):
    """A session with Github"""

    def __init__(self, user, proj):
        """Initialize a Github session"""
        auth_hdr = {"Authorization" : "token " + input("Enter PA token: ")}
        self._session = requests.Session()
        self._session.headers.update(auth_hdr)
        self._base = "https://api.github.com/repos/{}/{}".format(user, proj)

    def _get_labels(self):
        """Return labels"""
        # Returns list of labels in json
        data = self._session.get(self._base + "/labels").json()
        labels = []
        for lbl in data:
            labels.append(
                Label(lbl['name'], lbl['color'], lbl.get("description", ""))
            )
        return labels

    def _get_issues(self, comments=True):
        """Returns issues"""
        params = {"direction" : "asc"}
        data = self._session.get(self._base + "/issues", params=params).json()
        issues = []
        for item in data:
            issue = Issue(item['title'], item['body'], item['labels'])
            if item['comments'] > 0:
                issue._comments = self._get_comments(item['number'])
            issues.append(issue)
        return issues

    def _get_comments(self, issue_id):
        """Returns comments from issue"""
        data = self._session.get(self._base + "/issues/{}/comments".format(issue_id))
        data = data.json()
        comments = []
        for item in data:
            comments.append(
                Comment(item['user']['login'], item['body'])
            )
        return comments

    def _apply_label(self, label):
        """Upload a label to the web"""
        data = {
            "name" : label.title,
            "description" : label.desc,
            "color" : label.color
        }
        resp = self._session.post(
            self._base + "/labels", data=json.dumps(data))
        log.resp(resp.text)

    def _apply_issue(self, issue):
        """Upload an issue to the web"""
        data = {
            "title" : issue._title,
            "body" : issue._desc,
            "labels" : issue._labels
        }
        resp = self._session.post(
            self._base + "/issues", data=json.dumps(data))
        log.resp(resp.text)
        log.info(issue._comments)
        iss_number = resp.json()['number']
        for comment in issue._comments:
            data = {"body" : comment._body}
            resp = self._session.post(
                self._base + "/issues/{}/comments".format(iss_number),
                data=json.dumps(data))
            log.resp(resp.text)

    def _delete_all_labels(self):
        """Delete all labels"""
        data = self._session.get(self._base + "/labels").json()
        if not data:
            log.info("No labels found!")
        for item in data:
            resp = self._session.delete(
                self._base + "/labels/{}".format(item['name']))
            if resp.status_code == 204:
                log.resp("204: Deleted " + item['name'])
            else:
                log.resp("{}: {}".format(resp.status_code, resp.text))
