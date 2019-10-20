from decimal import Decimal

from constants import GBP, EUR
from product import Price, Product


def test_price():
    Product.objects.clear()
    Price.objects.clear()

    parent = Product()
    parent.save()

    product = Product()
    product.save()

    price_gbp = Price(product, Decimal('100.00'), GBP)
    price_gbp.save()

    assert product.get_price(GBP) is price_gbp.amount
    assert product.get_price(EUR) == price_gbp.amount * Decimal('1.16')

    product.parent_id = parent.id
    product.save()

    assert product.get_price(GBP) == price_gbp.amount
    assert product.get_price(EUR) == price_gbp.amount * Decimal('1.16')
