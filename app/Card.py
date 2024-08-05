"""Card: class for cards
"""


class Card(object):
    """Card: class for cards"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return
