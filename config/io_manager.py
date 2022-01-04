from datetime import date
from model.pool_model import PoolModel
import json


def write_pool_model(handle, pool_model) -> None:
    json_dict = PoolModel.to_json(pool_model)
    json.dump(json_dict, handle)


def read_pool_model(handle, current_day: date) -> PoolModel:
    json_dict = json.load(handle)
    return PoolModel(json_dict, current_day)


def write_config(handle, admin) -> None:
    pass


def read_config(handle, admin):
    pass


def write_price_list(source, target):
    pass


def get_pool_files(dictionary):
    pass
