from model.value_types import Price, Services, WeekDay, HoursRange
from model.price_list_model import PriceListPosition, PriceListModel
from datetime import time

# Tests for PriceListModel.__init__()

# @TODO: Write tests that check _read_pricing() and _pricing_validation()
# functionality

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
    pass


def test_price_list_model_init_wrong_json_keys():
    pass


def test_price_list_model_init_wrong_json_type():
    pass


def test_price_list_model_init_wrong_json_hours():
    pass


# Tests for PriceListModel.get_pricing()

def test_price_list_model_get_typical():
    pass


def test_price_list_model_get_wrong_service():
    pass
