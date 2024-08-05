from collections import OrderedDict
import os
import argparse
import configparser
import pandas as pd


def get_args() -> dict:
    """
    Get args from the command line

    Returns:
        dict: arguments from the command line

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config_file",
        type=str,
        default="config/main.ini",
        nargs="?",
        help="relative filepath to config from root",
    )
    args = parser.parse_args()
    return vars(args)


def get_params(level: str = ".") -> OrderedDict:
    """
    Get configuration parameters

    Args:
        level (str, optional): Level of the config file relative to where the function is called. Defaults to ".".

    Returns:
        OrderedDict: configuration parameters, organized into sections.

    """
    args = get_args()
    config_filename = args["config_file"]
    level = level
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )
    config.read(os.path.join(level, config_filename))

    params = OrderedDict()
    sections = ["paths"]
    for section in sections:
        params[section] = OrderedDict(config.items(section))
    return params


def load_card_data(
    data_dir: str, data_filename: str, template_filename: str
) -> pd.DataFrame:
    """
    Load card data from tsv

    Args:
        data_dir (str): Path to the data directory.
        data_filename (str): Name of the tsv.
        template_filename (str): Name of the template svg

    Returns:
        df (pd.DataFrame): card data.
        card_template: card template

    """
    filepath = os.path.join(data_dir, data_filename)
    df = pd.read_csv(filepath, sep="\t")

    df.columns = [c.lower() for c in df.columns]
    required_columns = ["title", "blurb", "category", "points"]
    assert set(required_columns) <= set(df.columns)

    filepath = os.path.join(data_dir, template_filename)
    with open(filepath) as f:
        card_template = f.read()

    return df, card_template


if __name__ == "__main__":
    params = get_params()
