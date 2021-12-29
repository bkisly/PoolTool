from model.value_types import Services, HoursRange, Price, WeekDay


class Reservation:
    def __init__(self, service, day, hours_range, price) -> None:
        self._data_validation(hours_range, price)

        self.service = Services(service)
        self.day = WeekDay(day)
        self.hours_range = hours_range
        self.price = price

    def _data_validation(self, hours_range, price):
        if not isinstance(hours_range, HoursRange):
            raise TypeError("Hours range must be an instance of HoursRange")

        if not isinstance(price, Price):
            raise TypeError("Price must be an instance of Price.")


class ReservationSystemModel:
    def __init__(self, price_list_model) -> None:
        self.reservations = []
        self._price_list_model = price_list_model

    def add_reservation(self, service, day, hours_range):
        pass

    def read_reservations(self):
        pass

    def write_reservations(self):
        pass
