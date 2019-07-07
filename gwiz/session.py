# session.py

from abc import ABC, abstractmethod as absmth

class Session(ABC):
    """A generic web session"""

    @absmth
    def get_labels(self, user, proj):
        pass

    @absmth
    def get_issues(self, user, proj):
        pass

    @absmth
    def post_labels(self, data):
        pass
