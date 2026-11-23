from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import urlsplit

from data.demo import BACKPACK, BIKE_LIGHT, BUYER
from pages.cart import CartPage
from pages.checkout import CheckoutPage


def test_checkout_items_amounts_and_confirmation(driver, inventory):
    prices = dict(inventory.products())
    selection = [BACKPACK, BIKE_LIGHT]
    for product in selection:
        inventory.add(product)
    inventory.open_cart()
    cart = CartPage(driver)
    assert sorted(cart.names()) == sorted(selection)
    cart.checkout()

    checkout = CheckoutPage(driver)
    checkout.enter_buyer(*BUYER)
    items = checkout.items()
    assert sorted(items) == sorted((name, 1, prices[name]) for name in selection)
    subtotal, tax, total = checkout.totals()
    assert subtotal == sum(prices[name] for name in selection)
    assert tax == (subtotal * Decimal("0.08")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    assert total == subtotal + tax

    assert checkout.finish() == "Thank you for your order!"
    assert urlsplit(driver.current_url).path == "/checkout-complete.html"
    assert checkout.wait_for_count(0)
