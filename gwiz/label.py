# label.py

class Label:

    def __init__(self, title, color, desc):
        self.title = title
        self.color = color
        self.desc = desc

    def as_dict(self):
        return {
            "title" : self.title,
            "color" : self.color,
            "desc" : self.desc
        }

    @staticmethod
    def json_to_labels(data):
        """Convert json structure to Labels"""
        labels = []
        for item in data:
            labels.append(Label(item['title'], item['color'], item['desc']))
        return labels
