from config.io_manager import (
    write_pool_model, read_pool_model,
    read_config, does_config_exist)
from config.admin import Admin
from model.pool_model import PoolModel
from view.operations_view import print_operations


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


def _add_reservation(pool_model: PoolModel):
    pass


def _view_reservations(pool_model: PoolModel):
    pass


def _view_price_list(pool_model: PoolModel):
    pass


def _view_working_hours(pool_model: PoolModel):
    pass


def _get_financial_report(pool_model: PoolModel):
    pass


def _view_tickets_amount(pool_model: PoolModel):
    pass


def _view_free_lanes(pool_model: PoolModel):
    pass


def pool_view(pool_path: str) -> None:
    pool_model = _pool_initialization(pool_path)
    print("POOLTOOL - POOL MANAGEMENT SYSTEM\n")
    print("Welcome to PoolTool!")
    print(
        f"Active pool: {pool_model.name}. "
        + f"Current day: {pool_model.current_day}\n")

    actions = [
        "Add reservation",
        "View reservations",
        "Price list",
        "Working hours",
        "Financial report",
        "Available tickets",
        "Available lanes",
        "Exit"
    ]

    exit_selected = False
    while not exit_selected:
        selected_index = print_operations(actions)

        match selected_index:
            case 0:
                _add_reservation(pool_model)
            case 1:
                _view_reservations(pool_model)
            case 2:
                _view_price_list(pool_model)
            case 3:
                _view_working_hours(pool_model)
            case 4:
                _get_financial_report(pool_model)
            case 5:
                _view_tickets_amount(pool_model)
            case 6:
                _view_free_lanes(pool_model)
            case 7:
                exit_selected = True
