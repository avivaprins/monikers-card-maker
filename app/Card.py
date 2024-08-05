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

        return

    def split_text(
        self,
        text: str,
        width: int = 40,
        max_lines: int = 8,
        pad_lines_flag: bool = True,
    ):
        text = textwrap.fill(text, width=width)
        lines = text.split("\n")

        n_lines = len(lines)
        assert n_lines <= max_lines
        # len_each_line = [len(l) for l in lines[: max_lines - 1]]
        # print(self.title)
        # print(len_each_line)
        # print(text)

        if n_lines < max_lines and max_lines > 2:
            warnings.warn(f'Card "{self.title}" has {n_lines} lines.')

        if pad_lines_flag:
            lines = lines + [""] * (max_lines - n_lines)

        return lines

    def generate_drawing(self, card_template: str):
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
            text=self.blurb, width=40, max_lines=8, pad_lines_flag=True
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
        filename = os.path.join(self.save_dir, f"svg/{self.name}.svg")
        with open(filename, "w") as f:
            f.write(self.svg)

        # svg_filename = filename
        # pdf_filename = os.path.join(self.save_dir, f"pdf/{self.name}.pdf")
        if pdf_flag:
            # svg2pdf(svg_filename, pdf_filename)
            drawing = svglib.svg2rlg(filename)
            filename = os.path.join(self.save_dir, f"pdf/{self.name}.pdf")
            renderPDF.drawToFile(drawing, filename, showBoundary=0)

        return
