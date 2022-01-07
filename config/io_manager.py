from datetime import date
from model.pool_model import PoolModel
from config.admin import Admin
import json


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
    # Check if there's a config.json file in the current directory.
    # Raise an exception if the given directory is not valid
    pass


def get_pools_files(current_directory: str) -> list:
    # Returns a list of .json files in the current directory with name
    # starting with "pool_"
    pass
