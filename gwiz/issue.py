# issues.py

class Issue:
    def __init__(self, title, desc, labels, state):
        self._title = title
        self._desc = desc
        self._labels = labels
        self._state = state
        self._comments = list()

    def add_comment(self, com):
        """Add comment to this issue's comment list"""
        self._comments.append(com)

    def as_dict(self):
        """Return this issue as a dict"""
        return {
            "title" : self._title,
            "desc" : self._desc,
            "labels" : self._labels,
            "state" : self._state,
            "comments" : [com.as_dict() for com in self._comments]
        }

    @staticmethod
    def json_to_issues(data):
        """Convert json to Issues"""
        issues = []
        for item in data:
            issue = Issue(item['title'], item['desc'], item['labels'], item['state'])
            issues.append(issue)
            for comment in item['comments']:
                issue.add_comment(Comment(comment['author'], comment['body']))
        return issues


class Comment:
    def __init__(self, author, body):
        self._author = author
        self._body = body

    def as_dict(self):
        return {
            "author" : self._author,
            "body" : self._body
        }
