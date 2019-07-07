# issues.py

class Issue:
    def __init__(self):
        self.title = None
        self.desc = None
        self.labels = None
        self.comments = None


class Comment:
    def __init__(self):
        self.author = None
        self.contents = None
