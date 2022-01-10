from model.price_list_model import PriceListModel
from model.reservations_model import ReservationSystemModel
from datetime import date, timedelta
from model.value_types import WeekDay, HoursRange
from exceptions.pool_model_exceptions import InvalidWorkingHoursError


class PoolModel:
    def __init__(self, initial_json_data: dict, current_day: date) -> None:
        # 1. Verify and assign pool data in JSON (including price list,
        # process solved by PriceListModel class) to the attributes.
        # 2. Create WorkingHours parser from JSON to the dict of
        # WeekDay -> HoursRange
        if not isinstance(current_day, date):
            raise TypeError("Current day must be an instance of date class")
        self.current_day = current_day

        self.name = initial_json_data["name"]
        self.working_hours = self._create_working_hours_dict(
            initial_json_data["working_hours"])
        self.lanes_amount = initial_json_data["lanes_amount"]

        if not str(self.lanes_amount).isdigit():
            raise TypeError(
                "Lanes amount must be an integer, positive number.")

        if self.lanes_amount < 3:
            raise ValueError("Lanes amount must be at least 3.")

        self.price_list_model = PriceListModel(
            self.working_hours, initial_json_data["price_list"])

        reservations = None

        if "reservations" in initial_json_data:
            reservations = initial_json_data["reservations"]

        self.reservation_system_model = ReservationSystemModel(
            self, reservations)

        # Current day is stored in a config file that is managed in the
        # admin mode

    def next_day(self) -> None:
        self.current_day += timedelta(days=1)

    @staticmethod
    def to_json(object) -> dict:
        json_dict = {}

        json_dict["name"] = object.name

        working_hours_json = {}

        for day in object.working_hours:
            working_hours_json[str(day.value)] = HoursRange.to_json(
                object.working_hours[day])

        json_dict["working_hours"] = working_hours_json
        json_dict["lanes_amount"] = object.lanes_amount
        json_dict["price_list"] = PriceListModel.to_json(
            object.price_list_model.get_pricing())
        json_dict["reservations"] = ReservationSystemModel.to_json(
            object.reservation_system_model.reservations)

        return json_dict

    def _create_working_hours_dict(self, working_hours_json: dict) -> dict:
        if not working_hours_json:
            raise InvalidWorkingHoursError("Working hours cannot be empty.")

        working_hours = {}

        for day in working_hours_json:
            week_day = WeekDay(int(day))

            if week_day in working_hours:
                raise InvalidWorkingHoursError(
                    "Working hours JSON must have unique day keys")

            hours_range = HoursRange.from_json(working_hours_json[day])

            if hours_range.durtation() < timedelta(hours=1):
                raise InvalidWorkingHoursError(
                    "Pool must be open for at least 1 hour.")

            working_hours[week_day] = hours_range

        return working_hours
