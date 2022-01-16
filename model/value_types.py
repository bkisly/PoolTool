from enum import Enum
from exceptions.value_types_exceptions import HoursRangeError
from exceptions.value_types_exceptions import NegativePriceError
from datetime import time, timedelta


class Services(Enum):
    """
    An enumerable type representing pool's service type.
    """

    INDIVIDUAL = 0
    SWIMMING_SCHOOL = 1


class WeekDay(Enum):
    """
    An enumerable type representing the day of the week.
    """

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Price:
    """
    A class representing price. Stores information about the amount of zl and
    gr separately. Provides addition, subtraction, comparison
    and to-string operations.
    """

    def __init__(self, zl: int, gr: int) -> None:
        self._data_validation(zl, gr)
        self.zl = zl
        self.gr = gr

    def __add__(self, other):
        self_total_gr = self.get_total_gr()
        other_total_gr = self.get_total_gr(other)
        result_total_gr = self_total_gr + other_total_gr
        return Price(result_total_gr // 100, result_total_gr % 100)

    def __sub__(self, other):
        self_total_gr = self.get_total_gr()
        other_total_gr = self.get_total_gr(other)
        result_total_gr = self_total_gr - other_total_gr

        if result_total_gr < 0:
            message = "Result of price subtraction cannot be negative."
            raise NegativePriceError(message)

        return Price(result_total_gr // 100, result_total_gr % 100)

    def __eq__(self, other) -> bool:
        if self.gr == other.gr and self.zl == other.zl:
            return True
        else:
            return False

    def __lt__(self, other) -> bool:
        self_total_gr = self.get_total_gr()
        other_total_gr = self.get_total_gr(other)

        if self_total_gr < other_total_gr:
            return True
        else:
            return False

    def __gt__(self, other) -> bool:
        self_total_gr = self.get_total_gr()
        other_total_gr = self.get_total_gr(other)

        if self_total_gr > other_total_gr:
            return True
        else:
            return False

    def __le__(self, other) -> bool:
        self_total_gr = self.get_total_gr()
        other_total_gr = self.get_total_gr(other)

        if self_total_gr <= other_total_gr:
            return True
        else:
            return False

    def __ge__(self, other) -> bool:
        self_total_gr = self.get_total_gr()
        other_total_gr = self.get_total_gr(other)

        if self_total_gr >= other_total_gr:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.zl}.{self.gr:02} zł"

    @staticmethod
    def from_json(json_dict: dict):
        """
        Returns a Price object converted from the JSON-formatted dictionary.
        """

        zl = json_dict["zl"]
        gr = json_dict["gr"]
        return Price(zl, gr)

    @staticmethod
    def to_json(object) -> dict:
        """
        Converts a Price object to a JSON-formatted dictionary and returns it.
        """

        json_dict = {
            "zl": object.zl,
            "gr": object.gr
        }

        return json_dict

    def get_total_gr(self, price=None) -> int:
        """
        Calculates and returns total amount of gr of a Price object.
        If no object is given, returns self total gr.
        """

        if price is None:
            price = self

        return price.zl * 100 + price.gr

    def _data_validation(self, zl: int, gr: int) -> None:
        """
        Validates initial data and throws proper exception if given
        data is invalid.
        """

        if not (str(zl).isdigit() and str(gr).isdigit()):
            if zl < 0 or gr < 0:
                raise NegativePriceError("Price attributes cannot be negative")

            raise TypeError("Invalid type of a Price attribute")


class HoursRange:
    """
    A class representing range of hours. Stores information about begin time
    and end time. Provides addition, comparison and to-string operations.
    """

    def __init__(self, begin: time, end: time) -> None:
        self._data_validation(begin, end)

        self.begin = begin
        self.end = end

    def is_in_range(self, hour: time, include_bounds: bool = True) -> bool:
        """
        Returns True, if given time is between begin and end time of the
        HoursRange object. Include_bounds set to True makes the method return
        True in case if the given time is equal begin or end time of the
        HoursRange.
        """

        if not isinstance(hour, time):
            raise TypeError("Hour to compare must be time instance.")

        if include_bounds:
            if self.begin <= hour <= self.end:
                return True
        else:
            if self.begin < hour < self.end:
                return True

        return False

    def check_intersection(self, hours_range) -> bool:
        """
        Returns True, if the given HoursRange object intersects with the
        HoursRange from which the method is called.
        """

        if hours_range.begin < self.end and hours_range.end > self.begin:
            return True
        elif hours_range.begin == self.begin and hours_range.end == self.end:
            return True
        else:
            return False

    def durtation(self) -> timedelta:
        """
        Returns a timedelta object representing the duration between
        begin and end time of the HoursRange object.
        """

        hours = self.end.hour - self.begin.hour
        minutes = self.end.minute - self.begin.minute
        return timedelta(hours=hours, minutes=minutes)

    def __add__(self, other):
        if not (self.begin == other.end or self.end == other.begin):
            raise HoursRangeError(
                "Summed HoursRange objects cannot intersect or be disconnected"
            )

        result_begin = min(self.begin, other.begin)
        result_end = max(self.end, other.end)
        return HoursRange(result_begin, result_end)

    def __eq__(self, other) -> bool:
        if self.begin == other.begin and self.end == other.end:
            return True

        return False

    def __str__(self) -> str:
        begin_str = f"{self.begin.hour}:{self.begin.minute:02}"
        end_str = f"{self.end.hour}:{self.end.minute:02}"
        return f"{begin_str} - {end_str}"

    @staticmethod
    def from_json(json_dict: dict):
        """
        Converts a JSON-formatted dictionary to an HoursRange
        object and returns it.
        """

        begin_hour = json_dict["begin"]["hour"]
        begin_minute = json_dict["begin"]["minute"]
        end_hour = json_dict["end"]["hour"]
        end_minute = json_dict["end"]["minute"]

        return HoursRange(
            time(begin_hour, begin_minute), time(end_hour, end_minute))

    @staticmethod
    def to_json(object) -> dict:
        """
        Converts an HoursRange object to a JSON-formatted dictionary
        and returns it.
        """

        json_dict = {
            "begin": {
                "hour": object.begin.hour,
                "minute": object.begin.minute
            },
            "end": {
                "hour": object.end.hour,
                "minute": object.end.minute
            }
        }

        return json_dict

    def _data_validation(self, begin: time, end: time) -> None:
        """
        Validates initial data and throws proper exceptions if the given data
        is invalid.
        """

        if not (isinstance(begin, time) and isinstance(end, time)):
            raise TypeError("Begin and end hours must be time instances.")

        if end <= begin:
            raise HoursRangeError("End hour must be greater than begin.")

        if begin.minute % 30 != 0 or end.minute % 30 != 0:
            raise HoursRangeError("Hours must have minutes equal 0 or 30.")
