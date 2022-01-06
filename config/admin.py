from datetime import date, timedelta


class Admin:
    def __init__(self, current_day: date) -> None:
        if not isinstance(current_day, date):
            raise ValueError("Current day must be a date class instance")

        self.current_day = current_day

    def set_current_pool(self, path: str):
        self.current_pool_path = path

    def next_day(self):
        self.current_day += timedelta(days=1)
