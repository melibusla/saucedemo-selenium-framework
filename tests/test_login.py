import pytest

from pages.login_page import LoginPage


# L1 — Valid login (standard_user)
def test_valid_login(driver):
    pass


# L2 — Locked-out user
def test_locked_out_user(driver):
    pass


# L3 — Empty username
def test_empty_username(driver):
    pass


# L4 — Empty password
def test_empty_password(driver):
    pass


# L5 — Both fields empty
def test_both_fields_empty(driver):
    pass


# L6 — Invalid username/password combo
def test_invalid_credentials(driver):
    pass


# L7 — performance_glitch_user login (document expected delay, not a failure)
def test_performance_glitch_user_login(driver):
    pass
