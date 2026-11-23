from urllib.parse import urlsplit

import pytest

from data.demo import DEMO_PASSWORD, STANDARD_USER
from pages.inventory import InventoryPage
from pages.login import LoginPage


def test_valid_login_opens_inventory(driver):
    login = LoginPage(driver)
    login.open()
    login.login(STANDARD_USER, DEMO_PASSWORD)

    inventory = InventoryPage(driver)
    assert inventory.title == "Products"
    assert urlsplit(driver.current_url).path == "/inventory.html"
    assert inventory.products()


@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        pytest.param("locked_out_user", DEMO_PASSWORD, "Sorry, this user has been locked out.", id="locked"),
        pytest.param(STANDARD_USER, "wrong-password",
                     "Username and password do not match any user in this service", id="wrong-password"),
        pytest.param("", "", "Username is required", id="empty-fields"),
    ],
)
def test_invalid_login_shows_reason(driver, username, password, message):
    login = LoginPage(driver)
    login.open()
    login.login(username, password)

    assert login.error == f"Epic sadface: {message}"
    assert urlsplit(driver.current_url).path == "/"
