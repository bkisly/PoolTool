from model.value_types import Price, HoursRange, Services, WeekDay
from model.price_list_model import PriceListPosition
from datetime import time
import pytest


# Tests for PriceListPosition.__init__()

def create_price_list_pos(service, weekday, begin, end, zl, gr):
    hours_range = HoursRange(begin, end)
    price = Price(zl, gr)
    return PriceListPosition(service, weekday, hours_range, price)


def test_price_list_pos_typical():
    begin = time(12, 30)
    end = time(14, 30)

    position = create_price_list_pos(
        Services.INDIVIDUAL,
        WeekDay.FRIDAY,
        begin,
        end,
        2,
        40)

    assert position.service == Services.INDIVIDUAL
    assert position.day == WeekDay.FRIDAY
    assert position.hours_range.begin == begin
    assert position.hours_range.end == end
    assert position.price.zl == 2
    assert position.price.gr == 40


def test_price_list_pos_wrong_service():
    begin = time(12, 30)
    end = time(14, 30)

    with pytest.raises(ValueError):
        create_price_list_pos(
            3,
            WeekDay.FRIDAY,
            begin,
            end,
            2,
            40)


def test_price_list_pos_wrong_weekday():
    begin = time(12, 30)
    end = time(14, 30)

    with pytest.raises(ValueError):
        create_price_list_pos(
            Services.INDIVIDUAL,
            8,
            begin,
            end,
            2,
            40)


def test_price_list_pos_wrong_type():
    with pytest.raises(TypeError):
        PriceListPosition(1, 1, "abcd", "efgh")


# Tests for PriceListPosition.from_json()

def test_price_list_pos_from_json_correct():
    price = Price(5, 60)
    hours_range = HoursRange(time(7, 30), time(10, 0))

    pos_json = {
        "service": 0,
        "day": 1,
        "hours_range": HoursRange.to_json(hours_range),
        "price": Price.to_json(price)
    }

    price_list_pos = PriceListPosition.from_json(pos_json)

    assert price_list_pos.service == Services.INDIVIDUAL
    assert price_list_pos.day == WeekDay.TUESDAY
    assert price_list_pos.hours_range == hours_range
    assert price_list_pos.price == price


def test_price_list_pos_from_json_malformed():
    price = Price(5, 60)

    pos_json = {
        "serviceee": 0,
        "daay": 1,
        "price": Price.to_json(price)
    }

    with pytest.raises(KeyError):
        PriceListPosition.from_json(pos_json)


def test_price_list_pos_from_json_wrong_values():
    price = Price(5, 60)
    hours_range = HoursRange(time(7, 30), time(10, 0))

    pos_json = {
        "service": 9,
        "day": 1,
        "hours_range": HoursRange.to_json(hours_range),
        "price": Price.to_json(price)
    }

    with pytest.raises(ValueError):
        PriceListPosition.from_json(pos_json)


def test_price_list_pos_from_json_wrong_dict():
    with pytest.raises(TypeError):
        PriceListPosition.from_json("abcd")


# Tests for PriceListPosition.to_json()

def test_price_list_pos_to_json_correct():
    price = Price(5, 60)
    hours_range = HoursRange(time(7, 30), time(10, 0))

    expected_json = {
        "service": 0,
        "day": 1,
        "hours_range": HoursRange.to_json(hours_range),
        "price": Price.to_json(price)
    }

    price_list_pos = PriceListPosition(
        Services.INDIVIDUAL, WeekDay.TUESDAY, hours_range, price)

    assert PriceListPosition.to_json(price_list_pos) == expected_json


def test_price_list_pos_to_json_wrong_object():
    with pytest.raises(AttributeError):
        PriceListPosition.to_json("abcd")
