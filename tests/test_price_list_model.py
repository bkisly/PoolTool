from exceptions.price_list_exceptions import EmptyPriceListError
from exceptions.price_list_exceptions import PricingHoursError
from exceptions.value_types_exceptions import HoursRangeError

from model.value_types import Price, Services, WeekDay, HoursRange
from model.price_list_model import PriceListPosition, PriceListModel

from datetime import time
import pytest

# Tests for PriceListModel.__init__()

working_hours = {
    WeekDay.MONDAY: HoursRange(time(8, 0), time(18, 0)),
    WeekDay.TUESDAY: HoursRange(time(9, 0), time(18, 0)),
    WeekDay.WEDNESDAY: HoursRange(time(8, 0), time(18, 0)),
    WeekDay.FRIDAY: HoursRange(time(10, 0), time(17, 0)),
    WeekDay.SATURDAY: HoursRange(time(11, 0), time(15, 0)),
}


def test_price_list_model_init_correct():
    input_json = [
        # Monday

        {
            "service": 0,
            "day": 0,
            "hours_range": {
                "begin": {
                    "hour": 8,
                    "minute": 0
                },
                "end": {
                    "hour": 14,
                    "minute": 30
                }
            },
            "price": {
                "zl": 2,
                "gr": 30
            }
        },

        {
            "service": 0,
            "day": 0,
            "hours_range": {
                "begin": {
                    "hour": 14,
                    "minute": 30
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            "price": {
                "zl": 3,
                "gr": 30
            }
        },

        {
            "service": 1,
            "day": 0,
            "hours_range": {
                "begin": {
                    "hour": 8,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            "price": {
                "zl": 5,
                "gr": 30
            }
        },

        # Tuesday

        {
            "service": 0,
            "day": 1,
            "hours_range": {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            "price": {
                "zl": 2,
                "gr": 30
            }
        },

        {
            "service": 1,
            "day": 1,
            "hours_range": {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            "price": {
                "zl": 1,
                "gr": 30
            }
        },

        # Wednesday

        {
            "service": 0,
            "day": 2,
            "hours_range": {
                "begin": {
                    "hour": 8,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            "price": {
                "zl": 1,
                "gr": 15
            }
        },

        {
            "service": 1,
            "day": 2,
            "hours_range": {
                "begin": {
                    "hour": 8,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            "price": {
                "zl": 2,
                "gr": 30
            }
        },

        # Friday

        {
            "service": 0,
            "day": 4,
            "hours_range": {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 12,
                    "minute": 30
                }
            },
            "price": {
                "zl": 0,
                "gr": 30
            }
        },

        {
            "service": 0,
            "day": 4,
            "hours_range": {
                "begin": {
                    "hour": 12,
                    "minute": 30
                },
                "end": {
                    "hour": 17,
                    "minute": 0
                }
            },
            "price": {
                "zl": 2,
                "gr": 30
            }
        },

        {
            "service": 1,
            "day": 4,
            "hours_range": {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 14,
                    "minute": 30
                }
            },
            "price": {
                "zl": 5,
                "gr": 90
            }
        },

        {
            "service": 1,
            "day": 4,
            "hours_range": {
                "begin": {
                    "hour": 14,
                    "minute": 30
                },
                "end": {
                    "hour": 17,
                    "minute": 0
                }
            },
            "price": {
                "zl": 2,
                "gr": 30
            }
        },

        # Saturday

        {
            "service": 0,
            "day": 5,
            "hours_range": {
                "begin": {
                    "hour": 11,
                    "minute": 0
                },
                "end": {
                    "hour": 15,
                    "minute": 0
                }
            },
            "price": {
                "zl": 6,
                "gr": 30
            }
        },

        {
            "service": 1,
            "day": 5,
            "hours_range": {
                "begin": {
                    "hour": 11,
                    "minute": 0
                },
                "end": {
                    "hour": 15,
                    "minute": 0
                }
            },
            "price": {
                "zl": 7,
                "gr": 30
            }
        },
    ]

    expected_pricing = [
        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.MONDAY,
            HoursRange(time(8, 0), time(14, 30)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.MONDAY,
            HoursRange(time(14, 30), time(18, 0)), Price(3, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.MONDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(5, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.TUESDAY,
            HoursRange(time(9, 0), time(18, 0)), Price(2, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.TUESDAY,
            HoursRange(time(9, 0), time(18, 0)), Price(1, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.WEDNESDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(1, 15)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.WEDNESDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.FRIDAY,
            HoursRange(time(10, 0), time(12, 30)), Price(0, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.FRIDAY,
            HoursRange(time(12, 30), time(17, 0)), Price(2, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.FRIDAY,
            HoursRange(time(10, 0), time(14, 30)), Price(5, 90)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.FRIDAY,
            HoursRange(time(14, 30), time(17, 0)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.SATURDAY,
            HoursRange(time(11, 0), time(15, 0)), Price(6, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.SATURDAY,
            HoursRange(time(11, 0), time(15, 0)), Price(7, 30)),
    ]

    price_list_model = PriceListModel(working_hours, input_json)
    result_pricing = price_list_model.get_pricing()

    assert len(result_pricing) == len(expected_pricing)

    for res_pos, exp_pos in zip(result_pricing, expected_pricing):
        assert res_pos.service == exp_pos.service
        assert res_pos.day == exp_pos.day
        assert res_pos.hours_range == exp_pos.hours_range
        assert res_pos.price == exp_pos.price


def test_price_list_model_init_malformed_json():
    mal_json_1 = []

    mal_json_2 = [
        {
            "service": 0,
            "day": 4,
            "hours_range": 2,
            "price": 7.4
        }
    ]

    mal_json_3 = [
        {
            "service": 0,
            "day": 0,
            "hours_range": {
                "begin": 0,
                "end": 4
            },
            "price": {
                "zl": 4,
                "gr": 5
            }
        }
    ]

    with pytest.raises(EmptyPriceListError):
        PriceListModel(working_hours, mal_json_1)

    with pytest.raises(TypeError):
        PriceListModel(working_hours, mal_json_2)

    with pytest.raises(TypeError):
        PriceListModel(working_hours, mal_json_3)


def test_price_list_model_init_wrong_json_keys():
    wrong_json = [
        {
            "abcd": 0,
            "bcde": 1,
            "efgh": 2,
            "gher": 3,
        }
    ]

    with pytest.raises(KeyError):
        PriceListModel(working_hours, wrong_json)


def test_price_list_model_init_wrong_json_type():
    wrong_json_1 = {
        "service": 1,
        "day": 0,
        "hours_range": 0,
        "price": 5
    }

    wrong_json_2 = 45

    with pytest.raises(TypeError):
        PriceListModel(working_hours, wrong_json_1)

    with pytest.raises(TypeError):
        PriceListModel(working_hours, wrong_json_2)


def test_price_list_model_init_wrong_json_hours():
    test_working_hours = {
        WeekDay.MONDAY: HoursRange(time(9, 0), time(16, 0)),
        WeekDay.MONDAY: HoursRange(time(10, 30), time(17, 0))
    }

    wrong_json_1 = [
        # Monday

        {
            "service": 0,
            "day": 0,
            "hours_range": {
                "begin": {
                    "hour": 10,
                    "minute": 30
                },
                "end": {
                    "hour": 16,
                    "minute": 0
                }
            },
            "price": {
                "zl": 4,
                "gr": 50
            }
        },

        {
            "service": 1,
            "day": 0,
            "hours_range": {
                "begin": {
                    "hour": 10,
                    "minute": 30
                },
                "end": {
                    "hour": 16,
                    "minute": 0
                }
            },
            "price": {
                "zl": 4,
                "gr": 50
            }
        }
    ]

    wrong_json_2 = [
        # Monday

        {
            "service": 0,
            "day": 0,
            "hours_range": {
                "begin": {
                    "hour": 10,
                    "minute": 30
                },
                "end": {
                    "hour": 16,
                    "minute": 0
                }
            },
            "price": {
                "zl": 4,
                "gr": 50
            }
        },

        {
            "service": 0,
            "day": 0,
            "hours_range": {
                "begin": {
                    "hour": 12,
                    "minute": 30
                },
                "end": {
                    "hour": 17,
                    "minute": 0
                }
            },
            "price": {
                "zl": 4,
                "gr": 50
            }
        }
    ]

    with pytest.raises(PricingHoursError):
        PriceListModel(test_working_hours, wrong_json_1)

    with pytest.raises(HoursRangeError):
        PriceListModel(test_working_hours, wrong_json_2)


# Tests for PriceListModel.get_pricing()

def test_price_list_model_get_typical():
    price_list = [
        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.MONDAY,
            HoursRange(time(8, 0), time(14, 30)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.MONDAY,
            HoursRange(time(14, 30), time(18, 0)), Price(3, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.MONDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(5, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.TUESDAY,
            HoursRange(time(9, 0), time(18, 0)), Price(2, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.TUESDAY,
            HoursRange(time(9, 0), time(18, 0)), Price(1, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.WEDNESDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(1, 15)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.WEDNESDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.FRIDAY,
            HoursRange(time(10, 0), time(12, 30)), Price(0, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.FRIDAY,
            HoursRange(time(12, 30), time(17, 0)), Price(2, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.FRIDAY,
            HoursRange(time(10, 0), time(14, 30)), Price(5, 90)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.FRIDAY,
            HoursRange(time(14, 30), time(17, 0)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.SATURDAY,
            HoursRange(time(11, 0), time(15, 0)), Price(6, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.SATURDAY,
            HoursRange(time(11, 0), time(15, 0)), Price(7, 30)),
    ]

    price_list_model = PriceListModel(
        working_hours, PriceListModel.to_json(price_list))

    result_price_list = price_list_model.get_pricing()

    assert len(result_price_list) == len(price_list)

    for test_pos, res_pos in zip(price_list, result_price_list):
        assert test_pos.service == res_pos.service
        assert test_pos.day == res_pos.day
        assert test_pos.hours_range == res_pos.hours_range
        assert test_pos.price == res_pos.price

    ind_price_list = price_list_model.get_pricing(Services.INDIVIDUAL)

    for position in ind_price_list:
        assert position.service == Services.INDIVIDUAL

    schools_price_list = price_list_model.get_pricing(Services.SWIMMING_SCHOOL)

    for position in schools_price_list:
        assert position.service == Services.SWIMMING_SCHOOL


def test_price_list_model_get_wrong_service():
    price_list = [
        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.MONDAY,
            HoursRange(time(8, 0), time(14, 30)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.MONDAY,
            HoursRange(time(14, 30), time(18, 0)), Price(3, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.MONDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(5, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.TUESDAY,
            HoursRange(time(9, 0), time(18, 0)), Price(2, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.TUESDAY,
            HoursRange(time(9, 0), time(18, 0)), Price(1, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.WEDNESDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(1, 15)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.WEDNESDAY,
            HoursRange(time(8, 0), time(18, 0)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.FRIDAY,
            HoursRange(time(10, 0), time(12, 30)), Price(0, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.FRIDAY,
            HoursRange(time(12, 30), time(17, 0)), Price(2, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.FRIDAY,
            HoursRange(time(10, 0), time(14, 30)), Price(5, 90)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.FRIDAY,
            HoursRange(time(14, 30), time(17, 0)), Price(2, 30)),

        PriceListPosition(
            Services.INDIVIDUAL, WeekDay.SATURDAY,
            HoursRange(time(11, 0), time(15, 0)), Price(6, 30)),

        PriceListPosition(
            Services.SWIMMING_SCHOOL, WeekDay.SATURDAY,
            HoursRange(time(11, 0), time(15, 0)), Price(7, 30)),
    ]

    price_list_model = PriceListModel(
        working_hours, PriceListModel.to_json(price_list))

    with pytest.raises(ValueError):
        price_list_model.get_pricing("abcd")

    with pytest.raises(ValueError):
        price_list_model.get_pricing(8)
