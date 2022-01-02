from datetime import date, time
from model.pool_model import PoolModel
from model.reservations_model import Reservation, ReservationSystemModel
import pytest

from model.value_types import HoursRange, Price, Services


pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
            0: {
                "begin": {
                    "hour": 8,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            1: {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            2: {
                "begin": {
                    "hour": 8,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            4: {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 17,
                    "minute": 0
                }
            },
            5: {
                "begin": {
                    "hour": 11,
                    "minute": 0
                },
                "end": {
                    "hour": 15,
                    "minute": 0
                }
            },
        },
        "price_list": [
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
            }
        ]
    }

pool_model = PoolModel(pool_json, date(2022, 1, 1))


# Tests for ReservationSystemModel.__init__()

def test_res_system_init_typical():
    reservation_system = ReservationSystemModel(pool_model)
    assert reservation_system.reservations == []


def test_res_system_init_wrong_pool_model():
    with pytest.raises(AttributeError):
        ReservationSystemModel(2)


# Tests for ReservationSystemModel.add_reservation():

def test_res_system_add_correct():
    reservation_system = ReservationSystemModel(pool_model)

    # Adding individual reservation with no hourly price changes

    reservation_system.add_reservation(
        Services.INDIVIDUAL, date(2022, 1, 3),
        HoursRange(time(9, 30), time(12, 0)))

    assert len(reservation_system.reservations) == 1

    reservation = reservation_system.reservations[0]
    assert reservation.get_service() == Services.INDIVIDUAL
    assert reservation.date == date(2022, 1, 3)
    assert reservation.hours_range == HoursRange(time(9, 30), time(12, 0))
    assert reservation.price == Price(5, 75)

    # Adding school reservation with no hourly price changes

    reservation_system.add_reservation(
        Services.SWIMMING_SCHOOL, date(2022, 1, 3),
        HoursRange(time(8, 0), time(17, 30)), 3)

    assert len(reservation_system.reservations) == 2

    reservation = reservation_system.reservations[1]
    assert reservation.get_service() == Services.SWIMMING_SCHOOL
    assert reservation.date == date(2022, 1, 3)
    assert reservation.hours_range == HoursRange(time(8, 0), time(17, 30))
    assert reservation.price == Price(50, 35)
    assert reservation.lane == 3

    # Adding individual reservation with hourly price changes

    reservation_system.add_reservation(
        Services.INDIVIDUAL, date(2022, 1, 7),
        HoursRange(time(11, 30), time(14, 0)))

    assert len(reservation_system.reservations) == 3

    reservation = reservation_system.reservations[2]
    assert reservation.get_service() == Services.INDIVIDUAL
    assert reservation.date == date(2022, 1, 7)
    assert reservation.hours_range == HoursRange(time(11, 30), time(14, 0))
    assert reservation.price == Price(3, 75)


def test_res_system_add_earlier_day():
    pass


def test_res_system_add_out_of_working_hours():
    pass


def test_res_system_add_incorrect_lane():
    pass


def test_res_system_add_no_tickets_available():
    pass


def test_res_system_add_taken_lane():
    pass


def test_res_system_add_decreasing_available_tickets():
    pass


def test_res_system_add_over_lanes_limit():
    pass


# Tests for ReservationSystemModel.calculate_total_income():

def test_res_system_total_income_typical():
    pass


def test_res_system_total_income_wrong_day():
    pass


def test_res_system_total_income_no_reservations():
    pass


# Tests for ReservationSystemModel.available_lanes():

def test_res_system_available_lanes_typical():
    pass


def test_res_system_available_lanes_wrong_day():
    pass


# Tests for ReservationSystemModel.is_lane_taken():

def test_res_system_lane_taken_typical():
    pass


def test_res_system_lane_taken_wrong_day():
    pass


def test_res_system_lane_taken_wrong_lane():
    pass


def test_res_system_lane_taken_no_reservations():
    pass


# Tests for ReservationSystemModel.reservations_amount():

def test_res_system_reservations_amount_typical():
    pass


def test_res_system_reservations_amount_wrong_day():
    pass


def test_res_system_reservations_amount_no_reservations():
    pass
