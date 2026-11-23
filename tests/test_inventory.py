def test_sort_by_price_then_descending_name(inventory):
    original = inventory.products()
    assert len({price for _, price in original}) > 1

    inventory.sort("lohi")
    by_price = inventory.products()
    assert sorted(by_price) == sorted(original)
    assert [price for _, price in by_price] == sorted(price for _, price in original)

    inventory.sort("za")
    assert inventory.products() == sorted(original, key=lambda item: item[0].casefold(), reverse=True)
