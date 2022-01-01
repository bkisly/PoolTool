from model.price_list_model import PriceListModel
from model.reservations_model import ReservationSystemModel
from datetime import date, datetime, timedelta


class PoolModel:
    def __init__(self, initial_json_data: dict) -> None:
        # 1. Verify and assign pool data in JSON (including price list,
        # process solved by PriceListModel class) to the attributes.
        # 2. Create WorkingHours parser from JSON to the dict of
        # WeekDay -> HoursRange
        self.name = initial_json_data["name"]
        self.working_hours = initial_json_data["working_hours"]
        self.lanes_amount = initial_json_data["lanes_amount"]
        self.price_list_model = PriceListModel(
            self._working_hours, initial_json_data["price_list"])
        self.reservation_system_model = ReservationSystemModel(self)

        # Find a way to make the current days
        # in all pool models be synchronized.

        self._current_day = date.today()

    def next_day(self):
        self._current_day += timedelta(days=1)
