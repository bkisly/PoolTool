from exceptions.reservation_exceptions import InvalidLaneError
from exceptions.reservation_exceptions import ReservationDurationError
from exceptions.reservation_exceptions import ReservationTimeTakenError
from model.value_types import Services, HoursRange, Price, WeekDay
from datetime import date, timedelta, datetime, time


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
            self, pool_model) -> None:

        self.reservations = []
        self._price_list = pool_model.price_list_model().get_pricing()
        self._current_day = pool_model.current_day()
        self._lanes_amount = pool_model.lanes_amount()
        self._woring_hours = pool_model.working_hours()

    def add_reservation(
            self, service: Services, date: date, hours_range: HoursRange):
        self._check_reservation_time(date, hours_range)

        # @TODO: Calculate the price for the reservation
        # Add new Reservation object to the list

    def calculate_total_income(self) -> Price:
        pass

    def _calculate_reservation_price(
            self, date: date, hours_range: HoursRange) -> Price:
        # Calculation is based on the sum of prices based on prices per hour
        # for particular hours ranges included in reservation hours range

        pass

    def _check_reservation_time(self, date: date, hours_range: HoursRange):
        # 1. Check if reservation date isn't earlier than the current day

        if date < self._current_day:
            raise ValueError("Reservation date must be current day or later.")

        # 2. Check if reservation time fits
        # pool working hours pool working hours

        week_day = WeekDay(date.weekday())
        available_hours = self._woring_hours[week_day]
        begin = hours_range.begin
        end = hours_range.end

        if not (available_hours.is_in_range(begin)
                and available_hours.is_in_range(end)):
            raise ValueError("Reservation time must fit working hours.")

        # 3. Check if there's not other reservation for this time. If yes,
        # propose new time for the reservation.

        if self._check_reservation_intersection(hours_range, date):
            proposed_date = self._propose_new_date(date, hours_range)
            raise ReservationTimeTakenError(
                proposed_date,
                f"""There's an existing reservation for the selected time.
                Closest possible reservation time with
                identical duration: {proposed_date}""")

    def _check_reservation_intersection(
            self, hours_range: HoursRange, date: date) -> bool:
        for reservation in self.reservations:
            if reservation.date == date:
                if reservation.hours_range.check_intersection(hours_range):
                    return True

        return False

    def _propose_new_date(self, date: date, hours_range: HoursRange):
        expected_duration = hours_range.durtation()
        start_time = datetime(
            date.year, date.month, date.day,
            hours_range.begin.hour, hours_range.begin.minute)

        date_found = False

        while not date_found:
            new_start = time(start_time.hour, start_time.minute)
            new_end = new_start + expected_duration
            new_weekday = WeekDay(start_time.weekday())
            available_hours = self._woring_hours[new_weekday]

            if (available_hours.is_in_range(new_start)
                    and available_hours.is_in_range(new_end)):

                new_range = HoursRange(new_start, new_end)
                if not self._check_reservation_intersection(
                        new_range, start_time.date()):

                    date_found = True

            if not date_found:
                start_time += timedelta(minutes=30)

        return start_time
