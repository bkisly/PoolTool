from config.io_manager import (
    write_pool_model, read_pool_model,
    read_config, does_config_exist)
from config.admin import Admin
from model.pool_model import PoolModel


def _config_initialization() -> Admin:
    if does_config_exist(".\\"):
        try:
            with open("config.json") as handle:
                admin = read_config(handle)
        except Exception as e:
            print("An error has occurred while loading the config file.")
            print(e.args[0])
            exit()
    else:
        print("There's no config file detected.")
        print(
            "If you run the program for the first time, "
            + "you need to do the initial configuration.")
        print(
            "Launch the program in admin mode (-a parameter) "
            + "and follow the instructions.")
        exit()

    return admin


def _pool_initialization(pool_path: str) -> PoolModel:
    admin = _config_initialization()

    try:
        with open(pool_path) as handle:
            pool_model = read_pool_model(handle, admin.current_day)
    except Exception as e:
        print("An error has occurred while reading the pool file.")
        print(str(e))
        exit()

    return pool_model


def _add_reservation():
    pass


def _view_reservations():
    pass


def _view_price_list():
    pass


def _view_tickets_amount():
    pass


def _view_free_lanes():
    pass


def pool_view(pool_path: str) -> None:
    pool_model = _pool_initialization(pool_path)
    print(pool_model.name)
    # @TODO: PoolModel reading done, continue with match-case for all options
