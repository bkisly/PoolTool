from model.value_types import HoursRange
from exceptions.value_types_exceptions import HoursRangeError
from datetime import time
import pytest


# Tests for HoursRange.__init__()

def test_hours_init_typical():
    hours = HoursRange(time(12, 0), time(14, 30))

    assert hours.begin.hour == 12
    assert hours.begin.minute == 0

    assert hours.end.hour == 14
    assert hours.end.minute == 30


def test_hours_init_wrong_minutes():
    with pytest.raises(HoursRangeError):
        HoursRange(time(12, 14), time(14, 0))


def test_hours_init_wrong_time_values():
    with pytest.raises(ValueError):
        HoursRange(time(-2, 9), time("abcd"))


def test_hours_init_end_less_or_equal_begin():
    with pytest.raises(HoursRangeError):
        HoursRange(time(12, 0), time(9, 0))

    with pytest.raises(HoursRangeError):
        HoursRange(time(12, 0), time(12, 0))


def test_hours_init_wrong_type():
    with pytest.raises(TypeError):
        HoursRange(12, "bc")


# Tests for HoursRange.is_in_range()

def test_hours_range_typical():
    compared_hour = time(12, 30)
    first_range = HoursRange(time(12, 0), time(13, 30))
    second_range = HoursRange(time(13, 0), time(14, 30))

    assert first_range.is_in_range(compared_hour)
    assert not second_range.is_in_range(compared_hour)


def test_hours_range_wrong_type():
    hours = HoursRange(time(9, 0), time(12, 0))

    with pytest.raises(TypeError):
        hours.is_in_range(234)


# Tests for HoursRange.check_intersection()

def test_hours_intersection_typical():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(11, 30), time(13, 0))
    third_range = HoursRange(time(7, 0), time(10, 30))

    assert first_range.check_intersection(second_range)
    assert first_range.check_intersection(third_range)
    assert not second_range.check_intersection(third_range)


def test_hours_intersection_one_inside_other():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(11, 30), time(12, 0))

    assert first_range.check_intersection(second_range)
    assert second_range.check_intersection(first_range)


def test_hours_intersection_ranges_equal():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(9, 0), time(12, 30))

    assert first_range.check_intersection(second_range)
    assert second_range.check_intersection(first_range)


def test_hours_intersection_equal_borders():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(12, 30), time(13, 0))
    third_range = HoursRange(time(7, 30), time(9, 0))

    assert not first_range.check_intersection(second_range)
    assert not first_range.check_intersection(third_range)


def test_hours_intersection_wrong_type():
    first_range = HoursRange(time(9, 0), time(12, 30))

    with pytest.raises(AttributeError):
        first_range.check_intersection(20)
