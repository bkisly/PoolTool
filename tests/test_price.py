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

    with pytest.raises(ValueError):
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
    return price + 2


# Tests for Price.__sub__()

def test_price_sub_typical():
    price_1 = Price(2, 47)
    price_2 = Price(1, 12)
    assert price_1 + price_2 == Price(5, 59)


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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
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

    with pytest.raises(ValueError):
        price_1 >= price_2
