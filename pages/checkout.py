from pages.base import BasePage, by_test_id, dollars


class CheckoutPage(BasePage):
    def enter_buyer(self, first, last, postal_code):
        self.visible("firstName").send_keys(first)
        self.visible("lastName").send_keys(last)
        self.visible("postalCode").send_keys(postal_code)
        self.click("continue")

    def items(self):
        self.visible("cart-list")
        return [
            (row.find_element(*by_test_id("inventory-item-name")).text,
             int(row.find_element(*by_test_id("item-quantity")).text),
             dollars(row.find_element(*by_test_id("inventory-item-price")).text))
            for row in self.driver.find_elements(*by_test_id("inventory-item"))
        ]

    def totals(self):
        return tuple(dollars(self.visible(field).text) for field in (
            "subtotal-label", "tax-label", "total-label"
        ))

    def finish(self):
        self.click("finish")
        return self.visible("complete-header").text
