"""Script to load card data and generate card drawings."""

import app.utils as utils
from app.Cards import Cards

import reportlab

if __name__ == "__main__":

    params = utils.get_params(level=".")
    reportlab.rl_config.TTFSearchPath.append(params["paths"]["data_dir"])

    card_data, card_template = utils.load_card_data(
        data_dir=params["paths"]["data_dir"],
        data_filename=params["paths"]["data_filename"],
        template_filename=params["paths"]["template_filename"],
    )

    cards = Cards(
        card_data=card_data.head(),
        card_template=card_template,
        save_dir=params["paths"]["card_dir"],
    )

    cards.save_to_pdf()
