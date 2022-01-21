from datetime import date, timedelta


class Admin:
    """
    A class capable of storing information about current day, so the initial
    config for the application. Provides methods to modify config data.
    """

    def __init__(self, current_day: date) -> None:
        if not isinstance(current_day, date):
            raise ValueError("Current day must be a date class instance")

        self.current_day = current_day

    def set_current_pool(self, path: str) -> None:
        self.current_pool_path = path

    def next_day(self) -> None:
        """
        Sets the current day for the next day.
        """

        self.current_day += timedelta(days=1)

    def previous_day(self) -> None:
        """
        Sets the current day for the previous day.
        """

        self.current_day -= timedelta(days=1)

    @staticmethod
    def to_json(object) -> dict:
        """
        Converts an Admin object to the JSON-formatted dictionary
        and returns it.
        """

        date = object.current_day
        date_dict = {
            "day": date.day,
            "month": date.month,
            "year": date.year
        }

        json_dict = {"current_day": date_dict}
        return json_dict

    @staticmethod
    def from_json(json_dict: dict):
        """
        Converts a JSON-formatted dictioanary to the Admin object
        and returns it.
        """

        date_dict = json_dict["current_day"]
        day = date_dict["day"]
        month = date_dict["month"]
        year = date_dict["year"]

        current_day = date(year, month, day)
        return Admin(current_day)
