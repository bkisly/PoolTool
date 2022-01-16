from model.reservations_model import Reservation, SchoolReservation
from model.value_types import Price, Services, HoursRange
from exceptions.reservation_exceptions import InvalidLaneError
from exceptions.reservation_exceptions import ReservationDurationError
from datetime import date, datetime, time
import pytest


# Tests for Reservation.__init__()

def test_reservation_init_typical():
    reservation = Reservation(
        date(2021, 12, 31), HoursRange(time(9, 0), time(10, 0)), Price(4, 50))

    assert reservation.get_service() == Services.INDIVIDUAL
    assert reservation.date == date(2021, 12, 31)
    assert reservation.hours_range == HoursRange(time(9, 0), time(10, 0))
    assert reservation.price == Price(4, 50)


def test_reservation_init_wrong_hours_range():
    with pytest.raises(ReservationDurationError):
        Reservation(
            date(2020, 12, 1),
            HoursRange(time(9, 0), time(9, 30)), Price(1, 20)
        )


def test_reservation_init_wrong_data_types():
    with pytest.raises(TypeError):
        Reservation(56, HoursRange(time(9, 0), time(10, 30)), Price(1, 20))

    with pytest.raises(TypeError):
        Reservation(date(2021, 12, 1), 56, Price(1, 20))

    with pytest.raises(TypeError):
        Reservation(
            date(2021, 12, 1), HoursRange(time(9, 0), time(10, 30)), 56)


# Tests for Reservation.is_in_datetime()

def test_reservation_datetime_typical():
    reservation = Reservation(
        date(2021, 12, 31), HoursRange(time(9, 0), time(10, 0)), Price(4, 50))
    date_time_correct = datetime(2021, 12, 31, 9, 30)
    date_time_wrong = datetime(2021, 12, 31, 10, 30)

    assert reservation.is_in_datetime(date_time_correct)
    assert not reservation.is_in_datetime(date_time_wrong)


def test_reservation_datetime_wrong_type():
    reservation = Reservation(
        date(2021, 12, 31), HoursRange(time(9, 0), time(10, 0)), Price(4, 50))
    date_time = 12

    with pytest.raises(AttributeError):
        reservation.is_in_datetime(date_time)


# Tests for Reservation.get_service()

def test_reservation_get_service():
    reservation = Reservation(
        date(2021, 12, 31), HoursRange(time(9, 0), time(10, 0)), Price(4, 50))

    assert reservation.get_service() == Services.INDIVIDUAL


def test_school_reservation_get_service():
    school_reservation = SchoolReservation(
            3, date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(2, 40))

    assert school_reservation.get_service() == Services.SWIMMING_SCHOOL


# Tests for Reservation.__str__()

def test_reservation_str():
    reservation = Reservation(
        date(2021, 12, 31), HoursRange(time(9, 0), time(15, 0)), Price(13, 46))

    expected_str_header = "Reservation for 2021-12-31 (9:00 - 15:00)"
    expected_str_info = "Individual, reservation cost: 13.46 zł"

    assert str(reservation) == f"{expected_str_header}\n{expected_str_info}"


# Tests for Reservation.from_json()

def test_reservation_from_json_correct():
    json_dict = {
        "service": 0,
        "date": {
            "day": 25,
            "month": 4,
            "year": 2021
        },
        "hours_range": {
            "begin": {
                "hour": 7,
                "minute": 30
            },
            "end": {
                "hour": 9,
                "minute": 0
            },
        },
        "price": {
            "zl": 5,
            "gr": 40
        }
    }

    reservation = Reservation.from_json(json_dict)

    assert reservation.get_service() == Services.INDIVIDUAL
    assert reservation.date == date(2021, 4, 25)
    assert reservation.hours_range == HoursRange(time(7, 30), time(9, 0))
    assert reservation.price == Price(5, 40)


def test_reservation_from_json_malformed():
    json_dict = {
        "service": 0,
        "asda": 56,
        "hours_rangeeee": 765,
    }

    with pytest.raises(KeyError):
        Reservation.from_json(json_dict)


def test_reservation_from_json_wrong_values():
    json_dict = {
        "service": "abcde",
        "date": 25,
        "hours_range": {
            "begin": {
                "hour": 7,
                "minute": 30
            },
            "end": {
                "hour": 9,
                "minute": 0
            },
        },
        "price": {
            "zl": 5,
            "gr": 40
        }
    }

    with pytest.raises(TypeError):
        Reservation.from_json(json_dict)


def test_reservation_from_json_wrong_dict():
    json_dict = 234

    with pytest.raises(TypeError):
        Reservation.from_json(json_dict)


# Tests for Reservation.to_json()

def test_reservation_to_json_correct():
    reservation = Reservation(
        date(2021, 12, 31), HoursRange(time(10, 30), time(15, 30)),
        Price(7, 80))

    expected_json = {
        "service": 0,
        "date": {
            "day": 31,
            "month": 12,
            "year": 2021
        },
        "hours_range": {
            "begin": {
                "hour": 10,
                "minute": 30
            },
            "end": {
                "hour": 15,
                "minute": 30
            },
        },
        "price": {
            "zl": 7,
            "gr": 80
        }
    }

    assert Reservation.to_json(reservation) == expected_json


def test_reservation_to_json_wrong_object():
    reservation = "sas"

    with pytest.raises(AttributeError):
        Reservation.to_json(reservation)


# Tests for SchoolReservation.__init__()

def test_school_reservation_init_typical():
    reservation = SchoolReservation(
            3, date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(2, 40))

    assert reservation.lane == 3
    assert reservation.get_service() == Services.SWIMMING_SCHOOL
    assert reservation.date == date(2021, 12, 1)
    assert reservation.hours_range == HoursRange(time(9, 0), time(10, 30))
    assert reservation.price == Price(2, 40)


def test_school_reservation_init_negative_lane():
    with pytest.raises(InvalidLaneError):
        SchoolReservation(
            -3, date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(2, 40))


def test_school_reservation_init_wrong_lane_type():
    with pytest.raises(InvalidLaneError):
        SchoolReservation(
            "abcd", date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(2, 40))


# Tests for SchoolReservation.from_json()

def test_school_reservation_from_json_correct():
    json_dict = {
        "service": 1,
        "lane": 5,
        "date": {
            "day": 25,
            "month": 4,
            "year": 2021
        },
        "hours_range": {
            "begin": {
                "hour": 7,
                "minute": 30
            },
            "end": {
                "hour": 9,
                "minute": 0
            },
        },
        "price": {
            "zl": 5,
            "gr": 40
        }
    }

    reservation = SchoolReservation.from_json(json_dict)

    assert reservation.get_service() == Services.SWIMMING_SCHOOL
    assert reservation.date == date(2021, 4, 25)
    assert reservation.hours_range == HoursRange(time(7, 30), time(9, 0))
    assert reservation.price == Price(5, 40)
    assert reservation.lane == 5


def test_school_reservation_from_json_malformed():
    json_dict = {
        "service": 0,
        "lanes": 15,
        "asda": 56,
        "hours_rangeeee": 765,
    }

    with pytest.raises(KeyError):
        SchoolReservation.from_json(json_dict)


def test_school_reservation_from_json_wrong_values():
    json_dict = {
        "service": "abcde",
        "lane": -18,
        "date": {
            "day": 25,
            "month": 4,
            "year": 2021
        },
        "hours_range": {
            "begin": {
                "hour": 7,
                "minute": 30
            },
            "end": {
                "hour": 9,
                "minute": 0
            },
        },
        "price": {
            "zl": 5,
            "gr": 40
        }
    }

    with pytest.raises(InvalidLaneError):
        SchoolReservation.from_json(json_dict)


def test_school_reservation_from_json_wrong_dict():
    json_dict = "abcd"

    with pytest.raises(TypeError):
        SchoolReservation.from_json(json_dict)


# Tests for SchoolReservation.to_json()

def test_school_reservation_to_json_correct():
    reservation = SchoolReservation(
        4, date(2021, 12, 31), HoursRange(time(10, 30), time(15, 30)),
        Price(7, 80))

    expected_json = {
        "service": 1,
        "lane": 4,
        "date": {
            "day": 31,
            "month": 12,
            "year": 2021
        },
        "hours_range": {
            "begin": {
                "hour": 10,
                "minute": 30
            },
            "end": {
                "hour": 15,
                "minute": 30
            },
        },
        "price": {
            "zl": 7,
            "gr": 80
        }
    }

    assert SchoolReservation.to_json(reservation) == expected_json


def test_school_reservation_to_json_wrong_object():
    reservation = 568

    with pytest.raises(AttributeError):
        SchoolReservation.to_json(reservation)


# Tests for SchoolReservation.__str__()

def test_school_reservation_str():
    reservation = SchoolReservation(
        4, date(2021, 12, 31), HoursRange(time(7, 0), time(9, 0)),
        Price(56, 89))

    expected_header = "Reservation for 2021-12-31 (7:00 - 9:00)"
    expected_info_1 = "Swimming school, lane number: 5, "
    expected_info_2 = "reservation cost: 56.89 zł"
    result = f"{expected_header}\n{expected_info_1}{expected_info_2}"

    assert str(reservation) == result
