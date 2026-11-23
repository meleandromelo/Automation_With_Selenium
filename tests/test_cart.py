from data.demo import BACKPACK, BIKE_LIGHT
from pages.cart import CartPage


def test_cart_count_and_items_persist(driver, inventory):
    inventory.add(BACKPACK)
    assert inventory.wait_for_count(1)
    inventory.add(BIKE_LIGHT)
    assert inventory.wait_for_count(2)
    inventory.open_cart()

    cart = CartPage(driver)
    assert sorted(cart.names()) == sorted([BACKPACK, BIKE_LIGHT])
    cart.remove(BACKPACK)
    assert cart.wait_for_count(1)
    cart.continue_shopping()
    inventory.visible("inventory-list")
    driver.refresh()
    assert inventory.wait_for_count(1)
    inventory.open_cart()
    assert cart.names() == [BIKE_LIGHT]

    cart.remove(BIKE_LIGHT)
    assert cart.wait_for_count(0)
    assert cart.names() == []
