from datetime import date, datetime, time
from model.pool_model import PoolModel
from model.reservations_model import ReservationSystemModel
from exceptions.reservation_exceptions import InvalidLaneError
from exceptions.reservation_exceptions import ReservationTimeTakenError
from exceptions.reservation_exceptions import ReservationDurationError
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


def test_res_system_add_too_short():
    reservation_system = ReservationSystemModel(pool_model)

    with pytest.raises(ReservationDurationError):
        reservation_system.add_reservation(
            Services.INDIVIDUAL, date(2022, 1, 7),
            HoursRange(time(11, 30), time(12, 0)))


def test_res_system_add_earlier_day():
    reservation_system = ReservationSystemModel(pool_model)

    with pytest.raises(ValueError):
        reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2021, 12, 31),
            HoursRange(time(12, 0), time(14, 0)), 1)


def test_res_system_add_out_of_working_hours():
    reservation_system = ReservationSystemModel(pool_model)

    with pytest.raises(ValueError):
        reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2022, 1, 1),
            HoursRange(time(12, 0), time(19, 0)), 1)


def test_res_system_add_incorrect_lane():
    reservation_system = ReservationSystemModel(pool_model)

    with pytest.raises(InvalidLaneError):
        reservation_system.add_reservation(
                Services.SWIMMING_SCHOOL, date(2022, 1, 1),
                HoursRange(time(12, 0), time(14, 0)), 8)

    with pytest.raises(InvalidLaneError):
        reservation_system.add_reservation(
                Services.SWIMMING_SCHOOL, date(2022, 1, 1),
                HoursRange(time(12, 0), time(14, 0)), -4)

    with pytest.raises(ValueError):
        reservation_system.add_reservation(
                Services.SWIMMING_SCHOOL, date(2022, 1, 1),
                HoursRange(time(12, 0), time(14, 0)), "abcd")


def test_res_system_add_no_tickets_available():
    pool_model.lanes_amount = 1
    reservation_system = ReservationSystemModel(pool_model)

    for i in range(5):
        reservation_system.add_reservation(
            Services.INDIVIDUAL, date(2022, 1, 3),
            HoursRange(time(9, 30), time(12, 0)))

    with pytest.raises(ReservationTimeTakenError) as e:
        reservation_system.add_reservation(
                Services.INDIVIDUAL, date(2022, 1, 3),
                HoursRange(time(9, 30), time(12, 0)))

    proposed_datetime = e.value.proposed_date
    assert proposed_datetime == datetime(2022, 1, 3, 12, 0)

    pool_model.lanes_amount = 5


def test_res_system_add_taken_lane():
    reservation_system = ReservationSystemModel(pool_model)

    reservation_system.add_reservation(
        Services.SWIMMING_SCHOOL, date(2022, 1, 3),
        HoursRange(time(8, 0), time(17, 30)), 3)

    with pytest.raises(ReservationTimeTakenError) as e:
        reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2022, 1, 3),
            HoursRange(time(10, 0), time(17, 30)), 3)

    proposed_datetime = e.value.proposed_date
    assert proposed_datetime == datetime(2022, 1, 4, 9, 0)


def test_res_system_add_decreasing_available_tickets():
    reservation_system = ReservationSystemModel(pool_model)

    for i in range(21):
        reservation_system.add_reservation(
            Services.INDIVIDUAL, date(2022, 1, 3),
            HoursRange(time(9, 30), time(12, 0)))

    with pytest.raises(ReservationTimeTakenError) as e:
        reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2022, 1, 3),
            HoursRange(time(10, 0), time(16, 0)), 3)

    proposed_datetime = e.value.proposed_date
    assert proposed_datetime == datetime(2022, 1, 3, 12, 0)


def test_res_system_add_over_lanes_limit():
    reservation_system = ReservationSystemModel(pool_model)

    reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2022, 1, 3),
            HoursRange(time(10, 0), time(16, 0)), 3)

    with pytest.raises(ReservationTimeTakenError) as e:
        reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2022, 1, 3),
            HoursRange(time(14, 30), time(17, 0)), 4)

    proposed_datetime = e.value.proposed_date
    assert proposed_datetime == datetime(2022, 1, 4, 9, 0)


# Tests for ReservationSystemModel.calculate_total_income():

def test_res_system_total_income_typical():
    pool_model.current_day = date(2022, 1, 3)
    reservation_system = ReservationSystemModel(pool_model)

    reservation_system.add_reservation(
        Services.INDIVIDUAL, date(2022, 1, 3),
        HoursRange(time(9, 30), time(12, 0)))

    reservation_system.add_reservation(
        Services.SWIMMING_SCHOOL, date(2022, 1, 3),
        HoursRange(time(8, 0), time(17, 30)), 3)

    reservation_system.add_reservation(
        Services.INDIVIDUAL, date(2022, 1, 7),
        HoursRange(time(11, 30), time(14, 0)))

    assert reservation_system.calculate_total_income() == Price(56, 10)
    pool_model.current_day = date(2022, 1, 1)


def test_res_system_total_income_no_reservations():
    reservation_system = ReservationSystemModel(pool_model)
    assert reservation_system.calculate_total_income() == Price(0, 0)


# Tests for ReservationSystemModel.available_lanes():

def test_res_system_available_lanes_typical():
    reservation_system = ReservationSystemModel(pool_model)

    reservation_system.add_reservation(
        Services.SWIMMING_SCHOOL, date(2022, 1, 3),
        HoursRange(time(8, 0), time(17, 30)), 3)

    date_time = datetime(2022, 1, 3, 10, 0)

    assert reservation_system.available_lanes(date_time) == [0, 1, 2, 4]


def test_res_system_available_lanes_wrong_day():
    reservation_system = ReservationSystemModel(pool_model)
    date_time = datetime(2021, 12, 30, 12, 30)

    with pytest.raises(ValueError):
        reservation_system.available_lanes(date_time)

    with pytest.raises(AttributeError):
        reservation_system.available_lanes("abcd")


# Tests for ReservationSystemModel.is_lane_taken():

def test_res_system_lane_taken_typical():
    reservation_system = ReservationSystemModel(pool_model)
    reservation_system.add_reservation(
        Services.SWIMMING_SCHOOL, date(2022, 1, 3),
        HoursRange(time(8, 0), time(17, 30)), 3)

    date_time_1 = datetime(2022, 1, 3, 12, 30)
    date_time_2 = datetime(2022, 1, 3, 17, 30)
    date_time_3 = datetime(2022, 1, 3, 18, 30)

    assert reservation_system.is_lane_taken(3, date_time_1)
    assert not reservation_system.is_lane_taken(3, date_time_2)
    assert not reservation_system.is_lane_taken(3, date_time_3)
    assert not reservation_system.is_lane_taken(1, date_time_1)


def test_res_system_lane_taken_wrong_day():
    reservation_system = ReservationSystemModel(pool_model)

    with pytest.raises(ValueError):
        reservation_system.is_lane_taken(3, datetime(2021, 12, 31, 7, 20))

    with pytest.raises(AttributeError):
        reservation_system.is_lane_taken(3, 345)


def test_res_system_lane_taken_wrong_lane():
    reservation_system = ReservationSystemModel(pool_model)

    with pytest.raises(InvalidLaneError):
        reservation_system.is_lane_taken(8, datetime(2022, 1, 1, 10, 30))

    with pytest.raises(InvalidLaneError):
        reservation_system.is_lane_taken(-4, datetime(2022, 1, 1, 10, 30))

    with pytest.raises(InvalidLaneError):
        reservation_system.is_lane_taken("sus", datetime(2022, 1, 1, 10, 30))


def test_res_system_lane_taken_no_reservations():
    reservation_system = ReservationSystemModel(pool_model)
    date_time = datetime(2022, 1, 3, 14, 0)
    assert not reservation_system.is_lane_taken(3, date_time)


# Tests for ReservationSystemModel.reservations_amount():

def test_res_system_reservations_amount_typical():
    reservation_system = ReservationSystemModel(pool_model)
    date_time = datetime(2022, 1, 3, 11, 0)

    for i in range(5):
        reservation_system.add_reservation(
            Services.INDIVIDUAL, date(2022, 1, 3),
            HoursRange(time(9, 30), time(12, 0)))

    reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2022, 1, 3),
            HoursRange(time(10, 0), time(16, 0)), 3)

    ind_amount = reservation_system.reservations_amount(
        Services.INDIVIDUAL, date_time)
    school_amount = reservation_system.reservations_amount(
        Services.SWIMMING_SCHOOL, date_time)

    assert ind_amount == 5
    assert school_amount == 1


def test_res_system_reservations_amount_wrong_day():
    reservation_system = ReservationSystemModel(pool_model)

    with pytest.raises(ValueError):
        reservation_system.reservations_amount(
            Services.INDIVIDUAL, datetime(2021, 12, 31, 7, 20))

    with pytest.raises(AttributeError):
        reservation_system.reservations_amount(Services.INDIVIDUAL, 345)


def test_res_system_reservations_amount_no_reservations():
    reservation_system = ReservationSystemModel(pool_model)
    date_time = datetime(2022, 1, 3, 11, 0)

    ind_amount = reservation_system.reservations_amount(
        Services.INDIVIDUAL, date_time)
    school_amount = reservation_system.reservations_amount(
        Services.SWIMMING_SCHOOL, date_time)

    assert ind_amount == 0
    assert school_amount == 0


# Tests for ReservationSystemModel.to_json()

def test_res_system_to_json_correct():
    reservation_system = ReservationSystemModel(pool_model)

    reservation_system.add_reservation(
        Services.INDIVIDUAL, date(2022, 1, 3),
        HoursRange(time(9, 30), time(12, 0)))

    reservation_system.add_reservation(
            Services.SWIMMING_SCHOOL, date(2022, 1, 3),
            HoursRange(time(10, 0), time(16, 0)), 3)

    expected_list = [
        {
            "service": 0,
            "date": {
                "day": 3,
                "month": 1,
                "year": 2022
            },
            "hours_range": {
                "begin": {
                    "hour": 9,
                    "minute": 30
                },
                "end": {
                    "hour": 12,
                    "minute": 0
                },
            },
            "price": {
                "zl": 5,
                "gr": 75
            }
        },
        {
            "service": 1,
            "lane": 3,
            "date": {
                "day": 3,
                "month": 1,
                "year": 2022
            },
            "hours_range": {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 16,
                    "minute": 0
                },
            },
            "price": {
                "zl": 31,
                "gr": 80
            }
        },
    ]

    assert ReservationSystemModel.to_json(
        reservation_system.reservations) == expected_list


def test_res_system_to_json_wrong_object():
    with pytest.raises(TypeError):
        ReservationSystemModel.to_json(245)
