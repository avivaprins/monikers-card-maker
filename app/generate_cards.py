import app.utils as utils
from app.Cards import Cards

from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
import reportlab

if __name__ == "__main__":

    params = utils.get_params(level=".")

    reportlab.rl_config.TTFSearchPath.append(params["paths"]["data_dir"])

    card_data, card_template = utils.load_card_data(
        data_dir=params["paths"]["data_dir"],
        data_filename=params["paths"]["data_filename"],
        template_filename=params["paths"]["template_filename"],
    )

    test = card_data.head()
    cards = Cards(
        card_data=test,
        card_template=card_template,
        save_dir=params["paths"]["card_dir"],
    )
    cards.save_cards()
