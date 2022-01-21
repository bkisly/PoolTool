from datetime import datetime


class ReservationDurationError(Exception):
    """
    An exception raised when a reservation duration is less than 1 hour.
    """
    pass


class InvalidLaneError(Exception):
    """
    An exception raised when selected lane number is out of lanes range.
    """
    pass


class ReservationTimeTakenError(Exception):
    """
    An exception raised when reservation time is taken. Stores information
    about closest possible reservation time.
    """

    def __init__(self, proposed_date: datetime = None, *args: object) -> None:
        self.proposed_date = proposed_date
        super().__init__(*args)
