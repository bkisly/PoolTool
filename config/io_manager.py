from datetime import date
from model.pool_model import PoolModel
from config.admin import Admin
import json
import os
import re


def write_pool_model(handle, pool_model) -> None:
    json_dict = PoolModel.to_json(pool_model)
    json.dump(json_dict, handle)


def read_pool_model(handle, current_day: date) -> PoolModel:
    json_dict = json.load(handle)
    return PoolModel(json_dict, current_day)


def write_config(handle, admin) -> None:
    json.dump(Admin.to_json(admin), handle)


def read_config(handle) -> Admin:
    json_dict = json.load(handle)
    return Admin.from_json(json_dict)


def does_config_exist(current_directory: str) -> bool:
    if current_directory[-1] != "\\" or current_directory[-1] != "/":
        current_directory += "/"

    return os.path.isfile(current_directory + "config.json")


def get_pools_files(current_directory: str) -> list:
    valid_json_files = []
    all_files = os.listdir(current_directory)

    for file in all_files:
        if ((re.fullmatch("pool_[0-9]{4}\.json", file) is not None)
                and os.path.isfile(current_directory + file)):
            valid_json_files.append(file)

    return valid_json_files
