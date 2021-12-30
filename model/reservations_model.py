from exceptions.reservation_exceptions import InvalidLaneError
from exceptions.reservation_exceptions import ReservationDurationError
from exceptions.reservation_exceptions import ReservationTimeTakenError
from model.value_types import Services, HoursRange, Price
from datetime import date, timedelta


class Reservation:
    def __init__(
            self, service: Services, date: date,
            hours_range: HoursRange, price: Price) -> None:

        self._data_validation(date, hours_range, price)
        self._validate_hours_range(hours_range)

        self.service = Services(service)
        self.date = date
        self.hours_range = hours_range
        self.price = price

    def _data_validation(self, day, hours_range, price):
        if not isinstance(day, date):
            raise TypeError("Date must be an instance of Date class.")

        if not isinstance(hours_range, HoursRange):
            raise TypeError("Hours range must be an instance of HoursRange")

        if not isinstance(price, Price):
            raise TypeError("Price must be an instance of Price.")

    def _validate_hours_range(self, hours_range: HoursRange):
        if hours_range.durtation() < timedelta(hours=1):
            raise ReservationDurationError(
                "Reservation must be at least 1 hour long.")


class SchoolReservation(Reservation):
    def __init__(
            self, lane: int, service: Services,
            date: date, hours_range: HoursRange, price: Price) -> None:

        if not str(lane).isdigit():
            raise InvalidLaneError("Lane must be a number greater or equal 0.")

        self.lane = lane
        super().__init__(service, date, hours_range, price)


class ReservationSystemModel:
    def __init__(
            self, price_list_model,
            current_day: date, lanes_amount: int) -> None:

        self.reservations = []
        self._price_list = price_list_model.get_pricing()
        self._current_day = current_day
        self._lanes_amount = lanes_amount

    def add_reservation(
            self, service: Services, date: date, hours_range: HoursRange):
        # VERIFICATION
        # 1. If type is okay \an element of Reservation constructor
        # 2. If date isn't past
        # 3. If hours range isn't out of working hours
        # 4. If reservation time isn't taken (propose closest time if taken)

        # RESERVATION
        # 1. Instantiate a new Reservation object
        # 2. Add it to the list of reservations
        pass

    def _check_reservation_time(self, date: date, hours_range: HoursRange):
        if date < self._current_day:
            raise ValueError("Reservation date must be current day or later.")
