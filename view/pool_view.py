from config.io_manager import (
    write_pool_model, read_pool_model,
    read_config, does_config_exist)
from config.admin import Admin
from model.pool_model import PoolModel
from view.operations_view import print_operations
from datetime import date, datetime, time, timedelta
from model.value_types import Services, HoursRange, WeekDay


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


def _save_pool_model(pool_model: PoolModel, pool_path: str) -> None:
    with open(pool_path) as f:
        file_name = f.name

    with open(file_name, "w") as handle:
        write_pool_model(handle, pool_model)


def _add_reservation(pool_model: PoolModel, pool_path: str) -> None:
    print("Adding new reservation...")
    valid_reservation = False
    services = [
        "Individual client",
        "Swimming school",
        "Cancel"
    ]

    while not valid_reservation:
        week_day = WeekDay(pool_model.current_day.weekday()).name.capitalize()
        print(f"Current day: {pool_model.current_day} ({week_day})")
        selected_service = print_operations(services, "Select service type:")

        if selected_service == 2:
            return
        elif selected_service == 1:
            selected_lane = input("Enter lane number: ")
        else:
            selected_lane = None

        selected_year = input("Enter reservation year: ")
        selected_month = input("Enter reservation month: ")
        selected_day = input("Enter reservation day: ")
        selected_begin_hour = input("Enter reservation begin hour: ")
        selected_begin_minute = input("Enter reservation begin minute: ")
        selected_end_hour = input("Enter reservation end hour: ")
        selected_end_minute = input("Enter reservation end minute: ")

        try:
            res_date = date(
                int(selected_year), int(selected_month), int(selected_day))
            res_service = Services(int(selected_service))
            begin_time = time(
                int(selected_begin_hour), int(selected_begin_minute))
            end_time = time(int(selected_end_hour), int(selected_end_minute))
            res_hours_range = HoursRange(begin_time, end_time)

            res_lane = int(
                selected_lane) - 1 if selected_lane is not None else None

            res_sys_model = pool_model.reservation_system_model
            reservation = res_sys_model.add_reservation(
                res_service, res_date, res_hours_range, res_lane)

            _save_pool_model(pool_model, pool_path)

        except Exception as e:
            print("An error has occurred while adding new reservation.")
            print(f"{e.args[0]} Try again.")
            continue

        valid_reservation = True

    print("\nSuccessfully added new reservation:")
    print(str(reservation) + "\n")


def _view_reservations(pool_model: PoolModel):
    actions = [
        "Reservations for individuals",
        "Reservations for schools",
        "All reservations"
    ]

    selected_index = print_operations(
        actions, "\nSelect which reservations do you want to get:")

    match selected_index:
        case 0:
            res_filter = Services.INDIVIDUAL
        case 1:
            res_filter = Services.SWIMMING_SCHOOL
        case 2:
            res_filter = None

    res_sys_model = pool_model.reservation_system_model

    reservations = res_sys_model.get_reservations(res_filter)
    res_amount = len(reservations)

    print(f"\nReservations amount: {res_amount}\n")

    index = 1
    for reservation in reservations:
        print(f"{index}. {reservation}\n")
        index += 1


def _view_price_list(pool_model: PoolModel):
    actions = [
        "Price list for individuals",
        "Price list for swimming schools",
        "Full price list"
    ]
    selected_index = print_operations(
        actions, "\nSelect which price list do you want to get:")

    match selected_index:
        case 0:
            pricing_filter = Services.INDIVIDUAL
        case 1:
            pricing_filter = Services.SWIMMING_SCHOOL
        case 2:
            pricing_filter = None

    price_list = pool_model.price_list_model.get_pricing(pricing_filter)

    print(f"\n{pool_model.name} price list:")
    for position in price_list:
        print(f"{position}")
    print()


def _view_working_hours(pool_model: PoolModel):
    working_hours = pool_model.working_hours
    print(f"\n{pool_model.name} working hours:")

    for day in working_hours:
        day_str = day.name.capitalize()
        print(f"{day_str}: {working_hours[day]}")

    print()


def _get_financial_report(pool_model: PoolModel):
    total_income = pool_model.reservation_system_model.calculate_total_income()
    print(
        f"\nCurrently, on {pool_model.current_day}"
        + f" pool's total income is {total_income}\n")


def _view_tickets_amount(pool_model: PoolModel):
    current_day = pool_model.current_day
    current_weekday = WeekDay(current_day.weekday())

    begin_time = pool_model.working_hours[current_weekday].begin
    end_time = pool_model.working_hours[current_weekday].end

    current_datetime = datetime.combine(current_day, begin_time)

    print("\nAvailable tickets for particular time periods:")

    while current_datetime.time() < end_time:
        current_begin = current_datetime.time()
        current_end = (current_datetime + timedelta(minutes=30)).time()
        current_range = HoursRange(current_begin, current_end)
        tickets = pool_model.reservation_system_model.available_tickets(
            current_datetime + timedelta(minutes=15))

        print(f"{current_range}: {tickets} tickets")
        current_datetime += timedelta(minutes=30)

    print()


def _view_free_lanes(pool_model: PoolModel):
    current_day = pool_model.current_day
    current_weekday = WeekDay(current_day.weekday())

    begin_time = pool_model.working_hours[current_weekday].begin
    end_time = pool_model.working_hours[current_weekday].end

    current_datetime = datetime.combine(current_day, begin_time)

    print("\nAvailable lanes for particular time periods:")

    while current_datetime.time() < end_time:
        current_begin = current_datetime.time()
        current_end = (current_datetime + timedelta(minutes=30)).time()
        current_range = HoursRange(current_begin, current_end)
        available_lanes = pool_model.reservation_system_model.available_lanes(
            current_datetime + timedelta(minutes=15))
        lanes_str = ""

        for lane in available_lanes[:-1]:
            lanes_str += f"{lane + 1}, "
        lanes_str += str(available_lanes[-1] + 1)

        print(f"{current_range}: lanes {lanes_str}")
        current_datetime += timedelta(minutes=30)

    print()


def pool_view(pool_path: str) -> None:
    pool_model = _pool_initialization(pool_path)
    week_day = WeekDay(pool_model.current_day.weekday()).name.capitalize()
    print("POOLTOOL - POOL MANAGEMENT SYSTEM\n")
    print("Welcome to PoolTool!")
    print(
        f"Active pool: {pool_model.name}. "
        + f"Current day: {pool_model.current_day} ({week_day})\n")

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
                _add_reservation(pool_model, pool_path)
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
