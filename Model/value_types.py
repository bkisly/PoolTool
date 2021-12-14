from enum import Enum


class Services(Enum):
    INDIVIDUAL = 0
    SWIMMING_SCHOOL = 1


class WeekDay(Enum):
    MONDAY = 0,
    TUESDAY = 1,
    WEDNESDAY = 2,
    THURSDAY = 3,
    FRIDAY = 4,
    SATURDAY = 5,
    SUNDAY = 6


class Price:
    def __init__(self, zl: int, gr: int) -> None:
        self.zl = zl
        self.gr = gr

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __eq__(self, other) -> bool:
        pass

    def __lt__(self, other) -> bool:
        pass

    def __gt__(self, other) -> bool:
        pass

    def __le__(self, other) -> bool:
        pass

    def __ge__(self, other) -> bool:
        pass


class HoursRange:
    def __init__(self, begin, end) -> None:
        self.begin = begin
        self.end = end

    def is_in_range(self, hour) -> bool:
        pass
