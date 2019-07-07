# github.py

import json
import requests

from gwiz.issue import Issue, Comment
from gwiz.label import Label
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
        data = self._session.get(self._base + "/issues").json()
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
        resp = self._session.post(self._base + "/labels", data=json.dumps(data))
        print(resp.text)
