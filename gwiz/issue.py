# issues.py

class Issue:
    def __init__(self, title, desc, labels):
        self._title = title
        self._desc = desc
        self._labels = labels
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
            "comments" : [com.as_dict() for com in self._comments]
        }


class Comment:
    def __init__(self, author, body):
        self._author = author
        self._body = body

    def as_dict(self):
        return {
            "author" : self._author,
            "body" : self._body
        }
