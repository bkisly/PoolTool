from model.reservations_model import Reservation, SchoolReservation
from model.value_types import Price, Services, HoursRange
from exceptions.reservation_exceptions import InvalidLaneError
from exceptions.reservation_exceptions import ReservationDurationError
from datetime import date, time
import pytest


# Tests for Reservation.__init__()

def test_reservation_init_typical():
    reservation = Reservation(
        Services.INDIVIDUAL, date(2021, 12, 31),
        HoursRange(time(9, 0), time(10, 0)), Price(4, 50)
    )

    assert reservation.service == Services.INDIVIDUAL
    assert reservation.date == date(2021, 12, 31)
    assert reservation.hours_range == HoursRange(time(9, 0), time(10, 0))
    assert reservation.price == Price(4, 50)


def test_reservation_init_wrong_hours_range():
    with pytest.raises(ReservationDurationError):
        Reservation(
            Services.SWIMMING_SCHOOL, date(2020, 12, 1),
            HoursRange(time(9, 0), time(9, 30)), Price(1, 20)
        )


def test_reservation_init_wrong_data_types():
    with pytest.raises(ValueError):
        Reservation(
            "abcd", date(2020, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(1, 20)
        )

    with pytest.raises(TypeError):
        Reservation(
            Services.SWIMMING_SCHOOL, 56,
            HoursRange(time(9, 0), time(10, 30)), Price(1, 20)
        )

    with pytest.raises(TypeError):
        Reservation(
            Services.SWIMMING_SCHOOL, date(2021, 12, 1),
            56, Price(1, 20)
        )

    with pytest.raises(TypeError):
        Reservation(
            Services.SWIMMING_SCHOOL, date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), 56
        )


# Tests for SchoolReservation.__init__()

def test_school_reservation_init_typical():
    reservation = SchoolReservation(
            3, Services.SWIMMING_SCHOOL, date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(2, 40)
        )

    assert reservation.lane == 3
    assert reservation.service == Services.SWIMMING_SCHOOL
    assert reservation.date == date(2021, 12, 1)
    assert reservation.hours_range == HoursRange(time(9, 0), time(10, 30))
    assert reservation.price == Price(2, 40)


def test_school_reservation_init_negative_lane():
    with pytest.raises(InvalidLaneError):
        SchoolReservation(
            -3, Services.SWIMMING_SCHOOL, date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(2, 40)
        )


def test_school_reservation_init_wrong_lane_type():
    with pytest.raises(InvalidLaneError):
        SchoolReservation(
            "abcd", Services.SWIMMING_SCHOOL, date(2021, 12, 1),
            HoursRange(time(9, 0), time(10, 30)), Price(2, 40)
        )
