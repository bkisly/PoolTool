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


# Tests for HoursRange.__add__()

def test_hours_range_add_typical():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(12, 30), time(13, 0))
    result = first_range + second_range
    assert result.begin == time(9, 0)
    assert result.end == time(13, 0)


def test_hours_range_add_intersecting():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(11, 30), time(13, 0))

    with pytest.raises(HoursRangeError):
        first_range + second_range


def test_hours_range_add_disconnected():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(13, 30), time(15, 0))

    with pytest.raises(HoursRangeError):
        first_range + second_range


def test_hours_range_add_wrong_type():
    first_range = HoursRange(time(9, 0), time(12, 30))

    with pytest.raises(AttributeError):
        first_range + 3


# Tests for HoursRange.__eq__()

def test_hours_range_eq_typical():
    first_range = HoursRange(time(9, 0), time(12, 30))
    second_range = HoursRange(time(9, 0), time(12, 30))
    third_range = HoursRange(time(12, 30), time(13, 0))

    assert first_range == second_range
    assert first_range != third_range


def test_hours_range_eq_wrong_type():
    first_range = HoursRange(time(9, 0), time(12, 30))

    with pytest.raises(AttributeError):
        first_range == 2


# Tests for HoursRange.__str__()

def test_hours_range_str_typical():
    hours_range = HoursRange(time(9, 30), time(12, 30))
    assert str(hours_range) == "9:30 - 12:30"


def test_hours_range_str_minutes_0():
    hours_range = HoursRange(time(9, 0), time(12, 30))
    assert str(hours_range) == "9:00 - 12:30"


def test_hours_range_str_hour_0():
    hours_range = HoursRange(time(0, 0), time(12, 30))
    assert str(hours_range) == "0:00 - 12:30"


# Tests for HoursRange.from_json()

def test_hours_range_from_json_correct():
    range_json = {
        "begin": {
            "hour": 5,
            "minute": 30
        },
        "end": {
            "hour": 8,
            "minute": 0
        }
    }

    assert HoursRange.from_json(range_json) == HoursRange(
        time(5, 30), time(8, 0))


def test_hours_range_from_json_malformed():
    range_json = {
        "begin": {
            "hour": 5,
            "minute": 30
        },
        "eeend": {
            "hour": 8,
            "minute": 0
        }
    }

    with pytest.raises(KeyError):
        HoursRange.from_json(range_json)


def test_hours_range_from_json_wrong_values():
    range_json = {
        "begin": {
            "hour": 5,
            "minute": 30
        },
        "end": {
            "hour": 6,
            "minute": 10
        }
    }

    with pytest.raises(HoursRangeError):
        HoursRange.from_json(range_json)


def test_hours_range_from_json_wrong_dict():
    with pytest.raises(TypeError):
        HoursRange.from_json("sas")


# Tests for HoursRange.from_json()

def test_hours_range_to_json_correct():
    hours_range = HoursRange(time(3, 30), time(5, 0))

    expected_json = {
        "begin": {
            "hour": 3,
            "minute": 30
        },
        "end": {
            "hour": 5,
            "minute": 0
        }
    }

    assert HoursRange.to_json(hours_range) == expected_json


def test_hours_range_to_json_wrong_object():
    with pytest.raises(AttributeError):
        HoursRange.to_json("uwu")
