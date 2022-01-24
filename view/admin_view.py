from datetime import date
from config.admin import Admin
from config.io_manager import read_config, write_config, does_config_exist
from view.operations_view import print_operations


def _config_validation() -> Admin:
    """
    Validates initial config and returns an instance of the Admin class
    based on the valid config.json file.
    """

    with open("config.json") as handle:
        try:
            admin = read_config(handle)
        except Exception as e:
            print("An error occurred while loading config file:")
            print({e.args[0]})
            exit()

    return admin


def _config_initialization() -> Admin:
    """
    Initializes config, saves it to the config.json file and returns an
    instance of the Admin class based on the given data.
    """

    print(
        "There's no config file detected, "
        + "preparing for the first launch...")
    print(
        "In order to launch the program properly, "
        + "you need to specify current day.")

    try:
        year = int(input("Enter current year: "))
        month = int(input("Enter current month: "))
        day = int(input("Enter current day: "))

        admin = Admin(date(int(year), int(month), int(day)))
    except Exception as e:
        print("An error occurred while creating config file.")
        print(f"{e.args[0]}")
        exit()

    with open("config.json", "w") as handle:
        write_config(handle, admin)

    print()
    return admin


def _config_write_and_confirmation(admin: Admin) -> None:
    with open("config.json", "w") as handle:
        write_config(handle, admin)

    print(
        "Successfully performed given operation. "
        + f"Current day: {admin.current_day}\n")


def _set_current_day(admin: Admin) -> None:
    try:
        year = int(input("Enter current year: "))
        month = int(input("Enter current month: "))
        day = int(input("Enter current day: "))

        new_day = date(year, month, day)
        admin.set_current_day(new_day)

        with open("config.json", "w") as handle:
            write_config(handle, admin)
    except Exception as e:
        print("An error has occurred while setting new day.")
        print(f"{e.args[0]}\n")
        return

    _config_write_and_confirmation(admin)


def _next_day(admin: Admin) -> None:
    admin.next_day()
    _config_write_and_confirmation(admin)


def _previous_day(admin: Admin) -> None:
    admin.previous_day()
    _config_write_and_confirmation(admin)


def admin_view() -> None:
    """
    Start point for the admin mode of the application. Handles user's
    interactions and calls proper functions.
    """

    admin = None

    if does_config_exist(".\\"):
        admin = _config_validation()
    else:
        admin = _config_initialization()

    print(f"PoolTool administration panel. Current day: {admin.current_day}")

    exit_selected = False
    while not exit_selected:
        selected_index = print_operations(
            ["Next day", "Previous day", "Set current day", "Exit"])

        match selected_index:
            case 0:
                _next_day(admin)
            case 1:
                _previous_day(admin)
            case 2:
                _set_current_day(admin)
            case 3:
                exit_selected = True
