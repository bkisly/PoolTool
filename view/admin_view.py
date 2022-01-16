from datetime import date
from config.admin import Admin
from config.io_manager import read_config, write_config, does_config_exist
from view.operations_view import print_operations


def _config_validation() -> Admin:
    with open("config.json") as handle:
        try:
            admin = read_config(handle)
        except Exception as e:
            print("An error occurred while loading config file:")
            print({e.args[0]})
            exit()

    return admin


def _config_initialization() -> Admin:
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


def admin_view() -> None:
    admin = None

    if does_config_exist(".\\"):
        admin = _config_validation()
    else:
        admin = _config_initialization()

    print(f"PoolTool administration panel. Current day: {admin.current_day}")

    exit_selected = False
    while not exit_selected:
        selected_index = print_operations(["Next day", "Previous day", "Exit"])

        if selected_index != 2:
            admin.next_day() if selected_index == 0 else admin.previous_day()

            with open("config.json", "w") as handle:
                write_config(handle, admin)

            print(
                "Successfully performed given operation. "
                + f"Current day: {admin.current_day}")
        else:
            exit_selected = True
