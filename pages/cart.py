from pages.base import BasePage, by_test_id


class CartPage(BasePage):
    def names(self):
        self.visible("cart-list")
        return [
            item.text for item in self.driver.find_elements(*by_test_id("inventory-item-name"))
        ]

    def remove(self, product):
        slug = product.lower().replace(" ", "-")
        self.click(f"remove-{slug}")

    def continue_shopping(self):
        self.click("continue-shopping")

    def checkout(self):
        self.click("checkout")
