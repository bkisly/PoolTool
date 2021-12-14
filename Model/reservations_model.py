class Reservation:
    def __init__(self, service, day, hours_range, price) -> None:
        self.service = service
        self.day = day
        self.hours_range = hours_range
        self.price = price


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
