"""Card: class for cards
"""

import os

# import statistics
import warnings
import textwrap
import re

from svglib import svglib
from reportlab.graphics import renderPDF


class Card(object):
    """Card: class for cards"""

    def __init__(self, card_template: str, save_dir: str, **kwargs):
        """


        Args:
            card_template (str): Template of the card, as an svg with placeholders.
            save_dir (str): Directory to save the drawn card.
            **kwargs: Additional card attributes, which may be required.

        Returns:
            None.

        """
        self.save_dir = save_dir
        for k, v in kwargs.items():
            setattr(self, k, v)

        colors = {
            1: "#57c599",
            2: "#2bbaf1",
            3: "#8459b3",
            4: "#f03c38",
        }
        self.color = colors[self.points]
        self.name = self.title.replace(" ", "_").lower()
        self.category = self.category.upper()
        self.points = str(self.points)
        self.svg = self.generate_drawing(card_template=card_template)
        self.filename = os.path.join(self.save_dir, f"pdf/{self.name}.pdf")

        return

    def split_text(
        self,
        text: str,
        width: int,
        max_lines: int,
        pad_lines_flag: bool,
    ):
        """
        Helper function that splits text into lines

        Args:
            text (str): Text, e.g. a blurb.
            width (int): Maximum character length of a line.
            max_lines (int): Maximum number of lines.
            pad_lines_flag (bool): Whether to pad lines until max_lines is reached.

        Returns:
            lines ([str]): Text, split into lines.

        """
        text = textwrap.fill(text, width=width)
        lines = text.split("\n")

        n_lines = len(lines)
        assert n_lines <= max_lines

        if n_lines < max_lines and max_lines > 2:
            warnings.warn(f'Card "{self.title}" has {n_lines} lines.')

        if pad_lines_flag:
            lines = lines + [""] * (max_lines - n_lines)

        return lines

    def generate_drawing(self, card_template: str):
        """
        Draws the card using the svg-style card template.

        Args:
            card_template (str): Template of the card, as an svg with placeholders.

        Returns:
            svg (str): Drawn card as svg.

        """
        svg = card_template
        svg = re.sub(r"{{color}}", self.color, svg)
        title = self.split_text(
            text=self.title, width=40, max_lines=2, pad_lines_flag=False
        )
        if len(title) == 1:
            replacements = {
                r"{{title}}": self.title,
                r"{{titleA}}": "",
                r"{{titleB}}": "",
            }
        else:
            replacements = {
                r"{{title}}": "",
                r"{{titleA}}": title[0],
                r"{{titleB}}": title[1],
            }
        for k, v in replacements.items():
            svg = re.sub(k, v, svg)

        blurb_text = self.split_text(
            text=self.blurb, width=35, max_lines=8, pad_lines_flag=True
        )
        for i, line in enumerate(blurb_text):
            regex = r"{{text" + str(i + 1) + r"}}"
            svg = re.sub(regex, line, svg)

        svg = re.sub(r"{{category}}", self.category, svg)
        svg = re.sub(r"{{score}}", self.points, svg)
        if int(self.points) > 1:
            svg = re.sub(r"{{points}}", "POINTS", svg)
        else:
            svg = re.sub(r"{{points}}", "POINT", svg)
        return svg

    def save(self, pdf_flag: bool = True):
        """
        Either save to svg or pdf file format.

        Args:
            pdf_flag (bool, optional): Whether to save as pdf. Defaults to True.

        Returns:
            None.

        """

        if pdf_flag:

            filename = os.path.join(self.save_dir, "pdf/temp/")
            os.makedirs(filename, exist_ok=True)
            filename = os.path.join(filename, f"{self.name}.svg")

            svg = self.svg
            svg = re.sub(r"Gotham Rounded Book", "GOTHAM_ROUNDED_BOOK", svg)
            svg = re.sub(r"Gotham Rounded Bold", "GOTHAM_ROUNDED_BOLD", svg)
            svg = re.sub(
                r"Gotham Rounded Medium", "GOTHAM_ROUNDED_MEDIUM", svg
            )
            svg = re.sub(r"stroke-opacity:0", "stroke-opacity:1", svg)
            with open(filename, "w") as f:
                f.write(svg)
            drawing = svglib.svg2rlg(filename)
            filename = os.path.join(self.save_dir, f"pdf/{self.name}.pdf")
            renderPDF.drawToFile(drawing, filename, showBoundary=0)
        else:
            filename = os.path.join(self.save_dir, "svg/")
            os.makedirs(filename, exist_ok=True)
            filename = os.path.join(filename, f"{self.name}.svg")
            with open(filename, "w") as f:
                f.write(self.svg)

        return
