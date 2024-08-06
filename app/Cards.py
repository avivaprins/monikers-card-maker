"""Cards: class for a collection of cards
"""

import os
import pandas as pd
from pypdf import PdfReader, PdfWriter, Transformation

from app.Card import Card


class Cards(object):
    """Cards: class for a collection of cards"""

    def __init__(
        self, card_data: pd.DataFrame, card_template: str, save_dir: str
    ):
        """


        Args:
            card_data (pd.DataFrame): Table of details for each card.
            card_template (str): Template of a card rendering, as an svg with placeholders.
            save_dir (str): Directory to save the drawn card.

        Returns:
            None.

        """
        cards = []
        for index, row in card_data.iterrows():
            card = Card(**row, card_template=card_template, save_dir=save_dir)
            cards = cards + [card]
        self.cards = cards
        self.save_dir = save_dir
        return

    def save_cards(self):
        for card in self.cards:
            card.save()

    def merge_cards(self, cards_per_width: int, cards_per_height: int):

        n_pages = len(self.cards) // (cards_per_width * cards_per_height) + 1

        writer = PdfWriter()
        c = 0
        for n in range(n_pages):
            destpage = writer.add_blank_page(
                width=612, height=791
            )  # letter paper, pixels at 72 ppi
            for x in range(cards_per_width):
                for y in range(cards_per_height):
                    card = self.cards[c]
                    reader = PdfReader(card.filename)
                    sourcepage = reader.pages[0]
                    destpage.merge_transformed_page(
                        sourcepage,
                        Transformation().translate(
                            x * sourcepage.mediabox.width,
                            y * sourcepage.mediabox.height,
                        ),
                    )
                    c += 1
                    if c == len(self.cards):
                        return writer
        return writer

    def write_to_pdf(
        self, cards_per_width: int = 3, cards_per_height: int = 3
    ):
        writer = self.merge_cards(
            cards_per_width=cards_per_width, cards_per_height=cards_per_height
        )
        # Write file
        filename = os.path.join(self.save_dir, "card_set.pdf")
        with open(filename, "wb") as fp:
            writer.write(fp)
