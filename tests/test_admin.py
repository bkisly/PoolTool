from config.admin import Admin
from datetime import date
import pytest


# Tests for Admin.__init__()

def test_admin_init_typical():
    admin = Admin(date(2022, 1, 1))
    assert admin.current_day == date(2022, 1, 1)


def test_admin_init_wrong_day_type():
    with pytest.raises(ValueError):
        Admin("abcds")
