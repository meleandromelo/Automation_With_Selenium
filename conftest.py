import base64
import re
from pathlib import Path

import pytest
import pytest_html
from selenium.common.exceptions import WebDriverException

from data.demo import DEMO_PASSWORD, STANDARD_USER
from pages.inventory import InventoryPage
from pages.login import LoginPage
from utils.browser import new_chrome


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Exibe a janela do Chrome.")


@pytest.fixture
def driver(pytestconfig):
    browser = new_chrome(headed=pytestconfig.getoption("--headed"))
    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def inventory(driver):
    login = LoginPage(driver)
    login.open()
    login.login(STANDARD_USER, DEMO_PASSWORD)
    page = InventoryPage(driver)
    page.visible("inventory-list")
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    browser = item.funcargs.get("driver")
    if not report.failed or browser is None:
        return

    name = re.sub(r"[^a-zA-Z0-9_.-]+", "_", item.nodeid)
    path = Path(item.config.rootpath) / "results" / "screenshots" / f"{name}-{report.when}.png"
    try:
        png = browser.get_screenshot_as_png()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(png)
    except (OSError, WebDriverException) as error:
        report.sections.append(("Screenshot", str(error)))
        return
    extras = getattr(report, "extras", [])
    extras.append(pytest_html.extras.png(base64.b64encode(png).decode("ascii"), name="Screenshot"))
    report.extras = extras
