from model.pool_model import PoolModel
from model.price_list_model import PriceListModel
from model.reservations_model import ReservationSystemModel
from datetime import date, time
from model.value_types import HoursRange
from exceptions.pool_model_exceptions import InvalidWorkingHoursError
import pytest


# Tests for PoolModel.__init__()

def test_pool_model_init_typical():
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
            0: {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            1: {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 30
                }
            },
        },
        "price_list": [
            {
                "service": 0,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 0,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
        ]
    }

    working_hours = {
        0: HoursRange(time(9, 0), time(18, 0)),
        1: HoursRange(time(10, 0), time(18, 30))
    }

    pool_model = PoolModel(pool_json, date.today())

    assert pool_model.name == "MyPool"
    assert pool_model.lanes_amount == 5

    assert len(working_hours) == len(pool_model.working_hours)
    for expected_day, day in zip(working_hours, pool_model.working_hours):
        assert (working_hours[expected_day] == pool_model.working_hours[day])

    assert isinstance(pool_model.price_list_model, PriceListModel)
    assert isinstance(
        pool_model.reservation_system_model, ReservationSystemModel)
    assert pool_model.current_day == date.today()


def test_pool_model_init_invalid_working_hours():
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
            0: {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            8: {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 30
                }
            },
        },
        "price_list": [
            {
                "service": 0,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 0,
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
                    "gr": 50
                }
            },
        ]
    }

    with pytest.raises(ValueError):
        PoolModel(pool_json, date.today())


def test_pool_model_init_too_short_working_hours():
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
            0: {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 9,
                    "minute": 30
                }
            },
        },
        "price_list": [
            {
                "service": 0,
                "day": 0,
                "hours_range": {
                    "begin": {
                        "hour": 9,
                        "minute": 0
                    },
                    "end": {
                        "hour": 9,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 0,
                "hours_range": {
                    "begin": {
                        "hour": 9,
                        "minute": 0
                    },
                    "end": {
                        "hour": 9,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
        ]
    }

    with pytest.raises(InvalidWorkingHoursError):
        PoolModel(pool_json, date.today())


def test_pool_model_init_empty_working_hours():
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
        },
        "price_list": [
        ]
    }

    with pytest.raises(InvalidWorkingHoursError):
        PoolModel(pool_json, date.today())


def test_pool_model_init_wrong_day():
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
            0: {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            1: {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 30
                }
            },
        },
        "price_list": [
            {
                "service": 0,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 0,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
        ]
    }

    with pytest.raises(TypeError):
        PoolModel(pool_json, 25)


def test_pool_model_init_invalid_lanes_amount():
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 1,
        "working_hours": {
            0: {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            1: {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 30
                }
            },
        },
        "price_list": [
            {
                "service": 0,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 0,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
        ]
    }

    with pytest.raises(ValueError):
        PoolModel(pool_json, date.today())

    pool_json["lanes_amount"] = -4

    with pytest.raises(TypeError):
        PoolModel(pool_json, date.today())

    pool_json["lanes_amount"] = "abcd"

    with pytest.raises(TypeError):
        PoolModel(pool_json, date.today())


# Tests for PoolModel.next_day()

def test_pool_model_next_day():
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
            0: {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            1: {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 30
                }
            },
        },
        "price_list": [
            {
                "service": 0,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 0,
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
                    "gr": 50
                }
            },
            {
                "service": 0,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
        ]
    }

    pool_model = PoolModel(pool_json, date(2022, 1, 1))
    pool_model.next_day()

    assert pool_model.current_day == date(2022, 1, 2)
