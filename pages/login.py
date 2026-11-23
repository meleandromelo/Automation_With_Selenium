from data.demo import BASE_URL
from pages.base import BasePage


class LoginPage(BasePage):
    def open(self):
        self.driver.get(BASE_URL)
        self.visible("login-button")

    def login(self, username, password):
        self.visible("username").send_keys(username)
        self.visible("password").send_keys(password)
        self.click("login-button")

    @property
    def error(self):
        return self.visible("error").text
