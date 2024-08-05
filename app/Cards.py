"""Cards: class for a collection of cards
"""

import pandas as pd

from app.Card import Card


class Cards(object):
    """Cards: class for a collection of cards"""

    def __init__(self, card_data: pd.DataFrame):
        cards = []
        for index, row in card_data.iterrows():
            card = Card(**row)
            cards = cards + [card]
        self.cards = cards
        return
