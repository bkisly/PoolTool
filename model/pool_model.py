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
        self.name = initial_json_data["name"]
        self.working_hours = self._create_working_hours_dict(
            initial_json_data["working_hours"])
        self.lanes_amount = initial_json_data["lanes_amount"]
        self.price_list_model = PriceListModel(
            self._working_hours, initial_json_data["price_list"])
        self.reservation_system_model = ReservationSystemModel(self)

        # Current day is stored in a config file that is managed in the
        # admin mode

        if not isinstance(current_day, date):
            raise TypeError("Current day must be an instance of date class")
        self._current_day = current_day

    def next_day(self) -> None:
        self._current_day += timedelta(days=1)

    def _create_working_hours_dict(self, working_hours_json: dict) -> dict:
        working_hours = {}

        for day in working_hours_json:
            week_day = WeekDay(day)

            if week_day in working_hours:
                raise InvalidWorkingHoursError(
                    "Working hours JSON must have unique day keys")

            hours_range = HoursRange.from_json(working_hours_json[day])
            working_hours[week_day] = hours_range

        return working_hours
