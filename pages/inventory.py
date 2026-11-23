from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base import BasePage, by_test_id, dollars


class InventoryPage(BasePage):
    @property
    def title(self):
        return self.visible("title").text

    def products(self):
        items = self.wait.until(
            EC.visibility_of_all_elements_located(by_test_id("inventory-item"))
        )
        return [
            (item.find_element(*by_test_id("inventory-item-name")).text,
             dollars(item.find_element(*by_test_id("inventory-item-price")).text))
            for item in items
        ]

    def sort(self, value):
        Select(self.visible("product-sort-container")).select_by_value(value)

    def add(self, product):
        slug = product.lower().replace(" ", "-")
        self.click(f"add-to-cart-{slug}")
