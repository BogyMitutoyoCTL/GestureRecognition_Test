"""
Event Class
TODO: COMMENT
"""


class Event(list):
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


if __name__ == "__main__":
    print("Nothing to run here. Please run ControllerClass.")
