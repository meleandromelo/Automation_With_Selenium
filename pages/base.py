from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def by_test_id(value):
    return By.CSS_SELECTOR, f'[data-test="{value}"]'


def dollars(text):
    return Decimal(text.rsplit("$", 1)[1].strip())


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)

    def visible(self, test_id):
        return self.wait.until(EC.visibility_of_element_located(by_test_id(test_id)))

    def click(self, test_id):
        self.wait.until(EC.element_to_be_clickable(by_test_id(test_id))).click()

    def wait_for_count(self, count):
        badge = by_test_id("shopping-cart-badge")
        if count == 0:
            return self.wait.until(EC.invisibility_of_element_located(badge))
        self.wait.until(EC.visibility_of_element_located(badge))
        return self.wait.until(lambda driver: driver.find_element(*badge).text == str(count))

    def open_cart(self):
        self.click("shopping-cart-link")
