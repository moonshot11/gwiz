# label.py

class Label:

    def __init__(self, title, color, desc):
        self.title = title
        self.color = color
        self.desc = desc

    @property
    def as_dict(self):
        return {
            "title" : self.title,
            "color" : self.color,
            "desc" : self.desc
        }
