from collections import OrderedDict
import os
import argparse
import configparser


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


if __name__ == "__main__":
    params = get_params()
