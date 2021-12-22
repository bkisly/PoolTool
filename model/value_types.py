from enum import Enum
from exceptions.value_types_exceptions import NegativePriceError


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
        self._data_validation(zl, gr)
        self.zl = zl
        self.gr = gr

    def __add__(self, other):
        self_total_gr = self._get_total_gr()
        other_total_gr = self._get_total_gr(other)
        result_total_gr = self_total_gr + other_total_gr
        return Price(result_total_gr // 100, result_total_gr % 100)

    def __sub__(self, other):
        self_total_gr = self._get_total_gr()
        other_total_gr = self._get_total_gr(other)
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
        self_total_gr = self._get_total_gr()
        other_total_gr = self._get_total_gr(other)

        if self_total_gr < other_total_gr:
            return True
        else:
            return False

    def __gt__(self, other) -> bool:
        self_total_gr = self._get_total_gr()
        other_total_gr = self._get_total_gr(other)

        if self_total_gr > other_total_gr:
            return True
        else:
            return False

    def __le__(self, other) -> bool:
        self_total_gr = self._get_total_gr()
        other_total_gr = self._get_total_gr(other)

        if self_total_gr <= other_total_gr:
            return True
        else:
            return False

    def __ge__(self, other) -> bool:
        self_total_gr = self._get_total_gr()
        other_total_gr = self._get_total_gr(other)

        if self_total_gr >= other_total_gr:
            return True
        else:
            return False

    def _get_total_gr(self, price=None):
        if price is None:
            price = self

        return price.zl * 100 + price.gr

    def _data_validation(self, zl, gr):
        if not (str(zl).isdigit() and str(gr).isdigit()):
            if zl < 0 or gr < 0:
                raise NegativePriceError("Price attributes cannot be negative")

            raise TypeError("Invalid type of a Price attribute")


class HoursRange:
    def __init__(self, begin, end) -> None:
        self.begin = begin
        self.end = end

    def is_in_range(self, hour) -> bool:
        pass
