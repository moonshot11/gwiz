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
        self._base = self.API_ROOT + "/repos/{}/{}".format(user, proj)

    @property
    def API_ROOT(self):
        return "https://api.github.com"

    def get_rate_limit(self):
        """Get the rate limit"""
        resp = self._session.get(self.API_ROOT + "/rate_limit")
        log.info(resp.text)

    def _get_labels(self):
        """Return labels"""
        # Returns list of labels in json
        data = self._get("/labels")
        labels = []
        for lbl in data:
            labels.append(
                Label(lbl['name'], lbl['color'], lbl.get("description", ""))
            )
        return labels

    def _get_issues(self, comments=True):
        """Returns issues"""
        params = {"direction" : "asc", "state" : "all"}
        data = self._get("/issues", params=params)
        issues = []
        for item in data:
            labels = [lbl['name'] for lbl in item['labels']]
            issue = Issue(item['title'], item['body'], labels, item['state'])
            if item['comments'] > 0:
                issue._comments = self._get_comments(item['number'])
            issues.append(issue)
        return issues

    def _get_comments(self, issue_id):
        """Returns comments from issue"""
        data = self._get("/issues/{}/comments".format(issue_id))
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
        log.info('Posting label "{}"...'.format(label.title), end='')
        resp = self._post(
            self._base + "/labels", data=self._format_data(data))
        print("done!")

    def _apply_issue(self, issue):
        """Upload an issue to the web"""
        data = {
            "title" : issue._title,
            "body" : issue._desc,
            "labels" : issue._labels
        }
        state = issue._state
        log.info('Posting issue "{}"...'.format(issue._title), end='')
        resp = self._post(
            self._base + "/issues", data=self._format_data(data))
        iss_number = resp.json()['number']
        # Update state
        if state == "closed":
            print("closing...", end='', flush=True)
            resp = self._patch(
                self._base + "/issues/" + str(iss_number),
                data=self._format_data({"state" : "closed"}))
        print("done!")
        # Add comments
        for comment in issue._comments:
            data = {"body" : comment._body}
            log.info("    Adding comment to issue #{}...".format(iss_number), end='')
            resp = self._post(
                self._base + "/issues/{}/comments".format(iss_number),
                data=self._format_data(data))
            print("done!")

    def _delete_all_labels(self):
        """Delete all labels"""
        data = self._get("/labels")
        if not data:
            log.info("No labels found!")
            return
        for item in data:
            resp = self._delete(
                self._base + "/labels/{}".format(item['name']))
            if resp.status_code == 204:
                log.resp("204: Deleted label " + item['name'])
            else:
                log.resp("{}: {}".format(resp.status_code, resp.text))

    def _delete_all_issues(self):
        """Delete all issues (including comments)"""
        log.info("Github API does not currently support deleting issues. Sorry!")
        return
        data = self._get("/issues")
        if not data:
            log.info("No issues found!")
            return
        for item in data:
            resp = self._delete(
                self._base + "/issues/{}".format(item['number']))
            if resp.status_code == 204:
                log.resp("204: Deleted issue " + item['title'])
            else:
                log.resp("{}: {}".format(resp.status_code, resp.text))

    def _format_data(self, data):
        """Dict -> format accepted by service"""
        return json.dumps(data)
