from datetime import date
from model.pool_model import PoolModel
from config.admin import Admin
import json
import os


def write_pool_model(handle, pool_model: PoolModel) -> None:
    """
    Writes PoolModel object to the given JSON file.
    """

    json_dict = PoolModel.to_json(pool_model)
    json.dump(json_dict, handle)


def read_pool_model(handle, current_day: date) -> PoolModel:
    """
    Reads PoolModel object from the given JSON file and returns it.
    """

    json_dict = json.load(handle)
    return PoolModel(json_dict, current_day)


def write_config(handle, admin: Admin) -> None:
    """
    Writes Admin object to the given JSON config file and returns it.
    """

    json.dump(Admin.to_json(admin), handle)


def read_config(handle) -> Admin:
    """
    Reads Admin object from the given JSON config file and returns it.
    """

    json_dict = json.load(handle)
    return Admin.from_json(json_dict)


def does_config_exist(current_directory: str) -> bool:
    """
    Checks if the config.json file exists in the current directory path
    and returns True if exists.
    """

    if current_directory[-1] != "\\" or current_directory[-1] != "/":
        current_directory += "/"

    return os.path.isfile(current_directory + "config.json")
