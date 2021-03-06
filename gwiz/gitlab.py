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
        # Get project ID
        projects = self._get("/users/{}/projects".format(user), base=self.API_ROOT)
        for item in projects:
            if item['name'] == proj:
                proj_id = item['id']
                log.info("Found project {}, id is {}".format(proj, proj_id))
                break
        else:
            log.error("Couldn't find project: " + proj)
        self._base = self.API_ROOT + "/projects/{}".format(proj_id)

    def get_rate_limit(self):
        """Gitlab rate limit"""
        log.error("Gitlab does not currently support rate limit reporting")

    @property
    def API_ROOT(self):
        return "https://gitlab.com/api/v4"

    def _get_labels(self):
        """Return labels"""
        data = self._get("/labels")
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
        data = self._get("/issues", params=params)
        issues = []
        for item in data:
            issue = Issue(item['title'], item['description'], item['labels'], item['state'])
            if item['user_notes_count'] > 0:
                issue._comments = self._get_comments(item['iid'])
            issues.append(issue)
        return issues

    def _get_comments(self, issue_id):
        params = {"sort" : "asc"}
        data = self._get(
            "/issues/{}/notes".format(issue_id),
            params=params)
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
        resp = self._post(
            self._base + "/labels", data=self._format_data(data))

    def _apply_issue(self, issue):
        """Upload an issue to Gitlab"""
        data = {
            "title" : issue._title,
            "description" : issue._desc,
            "labels" : ",".join(issue._labels)
        }
        state = issue._state
        resp = self._post(
            self._base + "/issues", data=self._format_data(data))
        iid = resp.json()['iid']
        if state == "closed":
            print("closing...", end='', flush=True)
            resp = self._put(
                self._base + "/issues/{}".format(iid),
                data=self._format_data({"state_event" : "close"}))
        return iid

    def _apply_comment(self, iid, comment):
        """Post comment to Gitlab issue"""
        data = {"body" : comment._body}
        resp = self._post(
            self._base + "/issues/{}/notes".format(iid),
            data=self._format_data(data))

    def _delete_all_labels(self):
        """Delete all labels in a Github project"""
        data = self._get("/labels")
        if not data:
            log.info("No labels found!")
            return
        for item in data:
            info = {"name" : item['name']}
            resp = self._delete(
                self._base + "/labels",
                data=self._format_data(info))
            if resp.status_code == 204:
                log.resp("204: Deleted label " + item['name'])
            else:
                log.resp("{}: {}".format(resp.status_code, resp.text))

    def _delete_all_issues(self):
        """Delete all issues in a Gitlab project"""
        data = self._get("/issues")
        if not data:
            log.info("No issues found!")
            return
        for item in data:
            resp = self._delete(
                self._base + "/issues/{}".format(item['iid']))
            if resp.status_code == 204:
                log.resp("204: Deleted issue " + item['title'])
            else:
                log.resp("{}: {}".format(resp.status_code, resp.text))

    def _format_data(self, data):
        """Dict -> format accepted by service"""
        return data
