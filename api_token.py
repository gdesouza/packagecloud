"""
api_token.py

MIT License
Copyright (c) 2020 Gustavo de Souza
Author: Gus de Souza
"""

import os
import json
import logging


def read_token_from_env():
    """Reads the token from environment variable PACKAGECLOUD_API_KEY
    Returns
    -------
    The API token string or a blank string if the variable does not exist
    """

    return os.environ.get('PACKAGECLOUD_API_KEY', '')


def read_token_from_file(config_file):
    """Reads the token from a config file
    Parameters
    ----------
    config_file: string
        The packagecloud configuration file path

    Returns
    -------
    The API token string or a blank string if the variable does not exist
    """

    if not os.path.isfile(config_file):
        return ''

    with open(config_file, "r") as file:
        contents = file.read()

    try:
        return json.loads(contents).get('token', '')
    except json.decoder.JSONDecodeError:
        message = f"Could not decode JSON in {config_file}"
        logging.warning(message)
        return ''


def load_token():
    """
    Load packagecloud token
    Try to use env var PACKAGECLOUD_API_KEY first (for jenkins jobs)
    If it is not set then try to read it from ~/.packagecloud
    Returns
    -------
    string
        The API token string or a blank string if the variable does not exist
    """
    home_dir = os.path.expanduser("~")
    cfg_file = os.path.join(home_dir, ".packagecloud")

    return read_token_from_env() or read_token_from_file(cfg_file)
