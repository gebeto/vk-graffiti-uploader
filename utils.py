import json
from exceptions import NoConfigError


CONFIG_FILE_NAME = "VKdata.json"


def read_config():
    try:
        file = open(CONFIG_FILE_NAME, "r")
    except FileNotFoundError:
        raise NoConfigError()
    file_data = json.load(file)
    return file_data


def save_config(**kwargs):
    json.dump(kwargs, open(CONFIG_FILE_NAME, "w"))
