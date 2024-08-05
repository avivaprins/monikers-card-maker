"""Cards: class for a collection of cards
"""

import pandas as pd

from app.Card import Card


class Cards(object):
    """Cards: class for a collection of cards"""

    def __init__(
        self, card_data: pd.DataFrame, card_template: str, save_dir: str
    ):
        cards = []
        for index, row in card_data.iterrows():
            card = Card(**row, card_template=card_template, save_dir=save_dir)
            cards = cards + [card]
        self.cards = cards
        return

    def save_cards(self):
        for card in self.cards:
            card.save()
