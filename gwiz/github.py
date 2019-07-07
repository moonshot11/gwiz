# github.py

import requests

from gwiz import session

class Github(session.Session):
    """A session with Github"""

    def __init__(self, user, proj):
        """Initialize a Github session"""
        auth_hdr = {"Authorization" : "token " + input("Enter PA token: ")}
        self._session = requests.Session()
        self._session.headers.update(auth_hdr)
        self._base = "https://api.github.com/repos/{}/{}".format(user, proj)

    def get_labels(self):
        """Return labels"""
        response = self._session.get(self._base + "/labels")
        print(response.text)
