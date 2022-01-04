import pytest
from model.value_types import Price
from exceptions.value_types_exceptions import NegativePriceError


# Tests for Price.__init__()

def test_price_init_typical():
    price = Price(2, 47)
    assert price.zl == 2
    assert price.gr == 47


def test_price_init_zero():
    price = Price(0, 0)
    assert price.zl == 0
    assert price.gr == 0


def test_price_init_negative_values():
    with pytest.raises(NegativePriceError):
        Price(-2, 9)

    with pytest.raises(NegativePriceError):
        Price(4, -1)


def test_price_init_wrong_type():
    with pytest.raises(TypeError):
        Price(2.4, 7.78)

    with pytest.raises(TypeError):
        Price("abcd", "efgh")


# Tests for Price.__eq__()

def test_price_eq_typical():
    price_1 = Price(3, 12)
    price_2 = Price(3, 12)
    assert price_1 == price_2


def test_price_eq_wrong_type():
    price_1 = Price(3, 14)
    price_2 = 3.45

    with pytest.raises(AttributeError):
        price_1 == price_2


# Tests for Price.__add__()

def test_price_add_typical():
    price_1 = Price(2, 47)
    price_2 = Price(3, 12)
    assert price_1 + price_2 == Price(5, 59)


def test_add_gr_over_zl():
    price_1 = Price(2, 47)
    price_2 = Price(3, 72)
    assert price_1 + price_2 == Price(6, 19)


def test_price_add_zero():
    price_1 = Price(2, 47)
    price_2 = Price(0, 0)
    assert price_1 + price_2 == Price(2, 47)


def test_price_add_wrong_type():
    price = Price(2, 45)

    with pytest.raises(AttributeError):
        price + 2


# Tests for Price.__sub__()

def test_price_sub_typical():
    price_1 = Price(2, 47)
    price_2 = Price(1, 12)
    assert price_1 - price_2 == Price(1, 35)


def test_price_sub_zero():
    price_1 = Price(2, 45)
    price_2 = Price(0, 0)
    assert price_1 - price_2 == Price(2, 45)


def test_price_sub_result_is_0():
    price_1 = Price(2, 45)
    price_2 = Price(2, 45)
    assert price_1 - price_2 == Price(0, 0)


def test_price_sub_result_is_negative():
    price_1 = Price(2, 45)
    price_2 = Price(3, 12)

    with pytest.raises(NegativePriceError):
        price_1 - price_2


def test_price_sub_wrong_type():
    price_1 = Price(2, 45)
    price_2 = 23

    with pytest.raises(AttributeError):
        price_1 - price_2


# Tests for Price.__lt__()

def test_price_lt_typical():
    price_1 = Price(2, 45)
    price_2 = Price(3, 45)
    assert price_1 < price_2


def test_price_lt_equal():
    price_1 = Price(2, 45)
    price_2 = Price(2, 45)
    assert not price_1 < price_2


def test_price_lt_wrong_type():
    price_1 = Price(2, 45)
    price_2 = 23

    with pytest.raises(AttributeError):
        price_1 < price_2


# Tests for Price.__gt__()

def test_price_gt_typical():
    price_1 = Price(2, 45)
    price_2 = Price(3, 45)
    assert price_2 > price_1


def test_price_gt_equal():
    price_1 = Price(2, 45)
    price_2 = Price(2, 45)
    assert not price_1 > price_2


def test_price_gt_wrong_type():
    price_1 = Price(2, 45)
    price_2 = 3

    with pytest.raises(AttributeError):
        price_1 > price_2


# Tests for Price.__le__()

def test_price_le_typical():
    price_1 = Price(2, 45)
    price_2 = Price(3, 45)
    assert price_1 <= price_2


def test_price_le_equal():
    price_1 = Price(2, 45)
    price_2 = Price(2, 45)
    assert price_1 <= price_2


def test_price_le_wrong_type():
    price_1 = Price(2, 45)
    price_2 = 1

    with pytest.raises(AttributeError):
        price_1 <= price_2


# Tests for Price.__ge__()

def test_price_ge_typical():
    price_1 = Price(2, 45)
    price_2 = Price(1, 45)
    assert price_1 >= price_2


def test_price_ge_equal():
    price_1 = Price(2, 45)
    price_2 = Price(2, 45)
    assert price_1 >= price_2


def test_price_ge_wrong_type():
    price_1 = Price(2, 45)
    price_2 = 3

    with pytest.raises(AttributeError):
        price_1 >= price_2


# Tests for Price.__str__()

def test_price_str_typical():
    price = Price(16, 78)
    assert str(price) == "16.78 zł"


def test_price_str_gr_less_than_10():
    price = Price(57, 4)
    assert str(price) == "57.04 zł"


def test_price_str_zl_0():
    price = Price(0, 14)
    assert str(price) == "0.14 zł"


def test_price_str_gr_0():
    price = Price(32, 0)
    assert str(price) == "32.00 zł"


def test_price_str_0():
    price = Price(0, 0)
    assert str(price) == "0.00 zł"


# Tests for Price.from_json()

def test_price_from_json_correct():
    price_json = {
        "zl": 12,
        "gr": 45
    }

    assert Price.from_json(price_json) == Price(12, 45)


def test_price_from_json_malformed():
    price_json = {
        "zl": 12,
        "grrrr": 45
    }

    with pytest.raises(KeyError):
        Price.from_json(price_json)


def test_price_from_json_wrong_values():
    price_json = {
        "zl": 12,
        "gr": -45
    }

    with pytest.raises(NegativePriceError):
        Price.from_json(price_json)


def test_price_from_json_wrong_dict():
    with pytest.raises(TypeError):
        Price.from_json(24)


# Tests for Price.to_json()

def test_price_to_json_correct():
    price = Price(2, 56)

    expected_json = {
        "zl": 2,
        "gr": 56
    }

    assert Price.to_json(price) == expected_json


def test_price_to_json_wrong_object():
    with pytest.raises(AttributeError):
        Price.to_json(25)
