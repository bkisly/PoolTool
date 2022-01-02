from datetime import datetime


class ReservationDurationError(Exception):
    pass


class InvalidLaneError(Exception):
    pass


class ReservationTimeTakenError(Exception):
    def __init__(self, proposed_date: datetime = None, *args: object) -> None:
        self.proposed_date = proposed_date
        super().__init__(*args)
