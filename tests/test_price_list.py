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
    with pytest.raises(ValueError):
        PriceListPosition(1, 1, "abcd", "efgh")
