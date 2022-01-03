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

# @TODO: write tests for JSON parsers
