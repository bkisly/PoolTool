from exceptions.reservation_exceptions import InvalidLaneError
from exceptions.reservation_exceptions import ReservationDurationError
from exceptions.reservation_exceptions import ReservationTimeTakenError
from model.value_types import Services, HoursRange, Price, WeekDay
from datetime import date, timedelta, datetime


class Reservation:
    """
    Represents a single reservation for individual client. Stores information
    about reservation date, hours range and reservation cost.
    """

    def __init__(
            self, date: date,
            hours_range: HoursRange, price: Price) -> None:

        self._data_validation(date, hours_range, price)
        self._validate_hours_range(hours_range)

        self.date = date
        self.hours_range = hours_range
        self.price = price

    def __str__(self) -> str:
        hours_str = str(self.hours_range)
        price_str = str(self.price)
        date_str = str(self.date)
        service_str = "Individual"

        header = f"Reservation for {date_str} ({hours_str})"
        info_str = f"{service_str}, reservation cost: {price_str}"

        return f"{header}\n{info_str}"

    def is_in_datetime(
            self, date_time: datetime, include_bounds: bool = True) -> bool:
        """
        Returns true, if the reservation hours range and date intersects with
        the given datetime object. Include_bounds set to True makes the method
        return True, if the begin or end time is equal the time of the given
        datetime (while the dates are equal as well).
        """

        if (self.date == date_time.date()
                and self.hours_range.is_in_range(
                    date_time.time(), include_bounds)):
            return True

        return False

    def get_service(self) -> Services:
        """
        Returns the service type of the reservation.
        """

        return Services.INDIVIDUAL

    @staticmethod
    def from_json(json_dict: dict):
        """
        Converts a JSON-formatted dictionary to the Reservation object
        and returns it.
        """

        date_dict = json_dict["date"]
        day = date_dict["day"]
        month = date_dict["month"]
        year = date_dict["year"]

        imported_date = date(year, month, day)
        hours_range = HoursRange.from_json(json_dict["hours_range"])
        price = Price.from_json(json_dict["price"])

        return Reservation(imported_date, hours_range, price)

    @staticmethod
    def to_json(object) -> dict:
        """
        Converts a Reservation object to the JSON-formatted dictionary
        and returns it.
        """

        json_dict = {}
        date_dict = {}

        date_dict["day"] = object.date.day
        date_dict["month"] = object.date.month
        date_dict["year"] = object.date.year

        json_dict["date"] = date_dict
        json_dict["hours_range"] = HoursRange.to_json(object.hours_range)
        json_dict["price"] = Price.to_json(object.price)
        json_dict["service"] = Services.INDIVIDUAL.value

        return json_dict

    def _data_validation(
        self, day: date, hours_range: HoursRange, price: Price
    ) -> None:
        """
        Validates reservation initial data and throws proper exceptions if the
        given data is invalid.
        """

        if not isinstance(day, date):
            raise TypeError("Date must be an instance of Date class.")

        if not isinstance(hours_range, HoursRange):
            raise TypeError("Hours range must be an instance of HoursRange")

        if not isinstance(price, Price):
            raise TypeError("Price must be an instance of Price.")

    def _validate_hours_range(self, hours_range: HoursRange) -> None:
        """
        Validates the reservation duration and throws an exception, if the
        reservation is less than 1 hour long.
        """

        if hours_range.durtation() < timedelta(hours=1):
            raise ReservationDurationError(
                "Reservation must be at least 1 hour long.")


class SchoolReservation(Reservation):
    """
    Represents a single reservation for swimming school. Stores information
    about reservation lane number, date, hours range and reservation cost.
    """

    def __init__(
            self, lane: int,
            date: date, hours_range: HoursRange, price: Price) -> None:

        if not str(lane).isdigit():
            raise InvalidLaneError("Lane must be a number greater or equal 0.")

        self.lane = lane
        super().__init__(date, hours_range, price)

    def __str__(self) -> str:
        hours_str = str(self.hours_range)
        price_str = str(self.price)
        date_str = str(self.date)
        service_str = "Swimming school"

        header = f"Reservation for {date_str} ({hours_str})"
        info_str_1 = f"{service_str}, lane number: {self.lane + 1}, "
        info_str_2 = f"reservation cost: {price_str}"

        return f"{header}\n{info_str_1}{info_str_2}"

    def get_service(self) -> Services:
        return Services.SWIMMING_SCHOOL

    @staticmethod
    def from_json(json_dict: dict):
        """
        Converts a JSON-formatted dictionary to the SchoolReservation object
        and returns it.
        """

        base = Reservation.from_json(json_dict)
        lane = json_dict["lane"]

        return SchoolReservation(lane, base.date, base.hours_range, base.price)

    @staticmethod
    def to_json(object) -> dict:
        """
        Converts a SchoolReservation object to the JSON-formatted dictionary
        and returns it.
        """

        json_dict = {}
        base_dict = Reservation.to_json(object)

        json_dict["lane"] = object.lane
        json_dict["date"] = base_dict["date"]
        json_dict["hours_range"] = base_dict["hours_range"]
        json_dict["price"] = base_dict["price"]
        json_dict["service"] = Services.SWIMMING_SCHOOL.value

        return json_dict


class ReservationSystemModel:
    """
    Represents the reservation system of the pool. Stores the list of
    all reservations. Provides adding new reservations, calculating total
    income and more. Must be initialized with given PoolModel and optionally
    with JSON-formatted reservations list which should be initially added.
    """

    def __init__(
            self, pool_model, reservations_json: list = None) -> None:

        self.reservations = self._create_reservations_list_from_json(
            reservations_json)
        self._price_list = pool_model.price_list_model.get_pricing()
        self._current_day = pool_model.current_day
        self._lanes_amount = pool_model.lanes_amount
        self._woring_hours = pool_model.working_hours

    def get_reservations(self, service: Services = None) -> list[Reservation]:
        """
        Returns the list of reservations. If the service is given, returns only
        reservations for individuals of swimming schools.
        """

        if service is None:
            return self.reservations
        else:
            reservations_to_return = []

            for reservation in self.reservations:
                if reservation.get_service() == service:
                    reservations_to_return.append(reservation)

            return reservations_to_return

    def add_reservation(
            self, service: Services, date: date,
            hours_range: HoursRange, lane: int = None) -> Reservation:
        """
        Adds new reservation and returns it. Adds reservation for individual
        client if the lane isn't given, otherwise adds reservation for swimming
        school.
        """

        # If a reservation can't be added due to the availability,
        # propose the closest possible date and time and pass
        # the raised exception. Otherwise pass other exceptions which occurred

        try:
            self._validate_reservation(date, hours_range, service, lane)
        except ReservationTimeTakenError:
            proposed_date = self._propose_new_date(
                date, hours_range, service, lane)

            raise ReservationTimeTakenError(
                proposed_date, f"""Given time for the reservation is not
                available. Closest possible reservation time under the same
                conditions: {proposed_date}""")
        except Exception:
            raise

        # Calculate the reservation price and add the object of proper type
        # to the reservations list

        price = self._calculate_reservation_price(date, hours_range, service)

        if service == Services.INDIVIDUAL:
            reservation = Reservation(date, hours_range, price)
        else:
            reservation = SchoolReservation(lane, date, hours_range, price)

        self.reservations.append(reservation)
        return reservation

    def calculate_total_income(self) -> Price:
        """
        Returns a Price object representing total income from the reservations
        of the current day.
        """

        total_income = Price(0, 0)

        for reservation in self.reservations:
            if reservation.date == self._current_day:
                total_income += reservation.price

        return total_income

    def available_lanes(self, date_time: datetime) -> list[int]:
        """
        Returns a list of available lane numbers for the given datetime.
        """

        if date_time.date() < self._current_day:
            raise ValueError("Given day cannot be earlier than current day.")

        lanes = list(range(self._lanes_amount))

        for reservation in self.reservations:
            if isinstance(reservation, SchoolReservation):
                if (reservation.is_in_datetime(date_time, False)
                        and reservation.lane in lanes):
                    lanes.remove(reservation.lane)

        return lanes

    def available_tickets(self, date_time: datetime) -> int:
        """
        Returns the amount of available tickets for the given datetime.
        """

        total_tickets = 5 * len(self.available_lanes(date_time))
        return total_tickets - self.reservations_amount(
            Services.INDIVIDUAL, date_time)

    def is_lane_taken(self, lane: int, date_time: datetime) -> bool:
        """
        Returns true, if the given lane number is taken for the given datetime.
        """

        if date_time.date() < self._current_day:
            raise ValueError("Given day cannot be earlier than current day.")

        if lane not in range(self._lanes_amount):
            raise InvalidLaneError(
                "Lane number must be between 0 and last lane ID.")

        for reservation in self.reservations:
            if isinstance(reservation, SchoolReservation):
                if (reservation.is_in_datetime(date_time, False)
                        and reservation.lane == lane):
                    return True

        return False

    def reservations_amount(
        self, service: Services, date_time: datetime
    ) -> int:
        """
        Returns the amount of reservations of the particular type
        for the given datetime.
        """

        if date_time.date() < self._current_day:
            raise ValueError("Given day cannot be earlier than current day.")

        amount = 0

        for reservation in self.reservations:
            if reservation.is_in_datetime(date_time, False):
                if reservation.get_service() == Services(service):
                    amount += 1

        return amount

    @staticmethod
    def to_json(reservations_list: list[Reservation]) -> list:
        """
        Converts a list of Reservation objects to the JSON-formatted list of
        reservations and returns it.
        """

        json_list = []

        for reservation in reservations_list:
            if isinstance(reservation, SchoolReservation):
                json_list.append(SchoolReservation.to_json(reservation))
            elif isinstance(reservation, Reservation):
                json_list.append(Reservation.to_json(reservation))

        return json_list

    def _calculate_reservation_price(
            self, date: date, hours_range: HoursRange,
            service: Services) -> Price:
        """
        Calculates the price of the reservation to be added
        (based on the price list) and returns it.
        """

        # 1. Selecting those PriceListPosition objects, that belong to the
        # particular reservation

        day = WeekDay(date.weekday())
        positions = []

        for position in self._price_list:
            if (hours_range.check_intersection(position.hours_range)
                    and position.day == day and position.service == service):
                positions.append(position)

        # 2. Adding parts of the price based on the reservation price for the
        # particular hour

        reservation_total_gr = 0
        current_time = hours_range.begin

        while current_time < hours_range.end:
            current_begin = current_time

            dt = datetime.combine(date, current_time)
            dt += timedelta(minutes=30)
            current_time = dt.time()

            current_range = HoursRange(current_begin, current_time)

            for position in positions:
                if current_range.check_intersection(position.hours_range):
                    current_position = position
                    break

            reservation_total_gr += current_position.price.get_total_gr() / 2

        return Price(
            int(reservation_total_gr // 100), int(reservation_total_gr % 100))

    def _validate_reservation(
            self, date: date, hours_range: HoursRange,
            service: Services, lane: int = None) -> None:
        """
        Validates the reservation data and throws proper exceptions in case of
        any incorrectness.
        """

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

        # 3. Check if the lane isn't greater than the amount of lanes

        if lane is not None and (int(lane) >= self._lanes_amount):
            raise InvalidLaneError(
                "Lane number must be in range of lanes amount.")

        # 4. Check the conditions regarding lanes amount,
        # available tickets etc.

        if self._check_reservation_intersection(
                hours_range, date, service, lane):
            raise ReservationTimeTakenError

    def _check_reservation_intersection(
            self, hours_range: HoursRange,
            date: date, service: Services, lane: int) -> bool:
        """
        Returns True if the given time for the reservation to be added
        is available.
        """

        current_time = hours_range.begin

        # Algorithm is checking every 30-minutes period of the
        # reservation from begin to end

        while current_time < hours_range.end:
            date_time = datetime(
                date.year, date.month, date.day,
                current_time.hour, current_time.minute)

            if service == Services.INDIVIDUAL:
                if self.available_tickets(date_time) == 0:
                    return True
            else:
                if self.is_lane_taken(lane, date_time):
                    return True

                # Check if lane reservation won't cause the situation, when
                # in some time number of tickets is below number of
                # individual reservations

                new_lanes_amount = len(self.available_lanes(date_time)) - 1
                if (5 * new_lanes_amount <
                        self.reservations_amount(
                            Services.INDIVIDUAL, date_time)):
                    return True

                # Check if number of taken lanes isn't over 35% of all lanes

                new_lanes_taken = self._lanes_amount - new_lanes_amount
                if new_lanes_taken > .35 * self._lanes_amount:
                    return True

            dt = datetime.combine(date, current_time)
            dt += timedelta(minutes=30)
            current_time = dt.time()

        return False

    def _propose_new_date(
            self, date: date, hours_range: HoursRange,
            service: Services, lane: int) -> datetime:
        """
        Returns the closest available datetime for the reservation to be added.
        """

        proposed_datetime = datetime(
            date.year, date.month, date.day,
            hours_range.begin.hour, hours_range.begin.minute)
        expected_duration = hours_range.durtation()
        date_found = False

        # Algorithm tries to find a fitting reservation under the same
        # conditions every next 30 minutes

        while not date_found:
            new_begin = proposed_datetime.time()

            dt_end = datetime.combine(date, new_begin)
            dt_end += expected_duration
            new_end = dt_end.time()

            # Algorithm proceeds until the valid reservation is found
            # and returns fitting combination of date and time

            try:
                new_range = HoursRange(new_begin, new_end)

                self._validate_reservation(
                    proposed_datetime.date(), new_range, service, lane)
            except Exception:
                proposed_datetime += timedelta(minutes=30)
                continue

            date_found = True

        return proposed_datetime

    def _create_reservations_list_from_json(
        self, reservations_json: list
    ) -> list[Reservation]:
        """
        Creates and returns a list of reservations based on a list of
        JSON-formatted Reservation objects.
        """

        reservations = []

        if reservations_json is not None:
            for reservation in reservations_json:
                if reservation["service"] == 0:
                    reservations.append(Reservation.from_json(reservation))
                else:
                    reservations.append(
                        SchoolReservation.from_json(reservation))

        return reservations
