from uuid import uuid4

from constants import BASE_CURRENCY
from fake_django import ObjectNotFound, Manager, Model
from utils import exchange


class PriceNotFound(Exception):
    pass


class Price(Model):
    objects = Manager()

    def __init__(self, product, amount, currency):
        self.id = uuid4()
        self.product = product
        self.product_id = product.id

        self.amount = amount
        self.currency = currency


class Pricing:
    def price_for(self, product, currency):
        try:
            price = Price.objects.get(product_id=product.id, currency=currency)
        except ObjectNotFound:
            price = Price.objects.get(
                product_id=product.parent_id, currency=currency
            )
        return price.amount


class Product(Model):
    objects = Manager()

    def __init__(self, parent_id=None):
        self.id = uuid4()
        self.parent_id = parent_id

        self._parent_cache = None

    def get_price(self, currency):
        try:
            return Pricing().price_for(self, currency)
        except ObjectNotFound:
            try:
                return exchange(Pricing().price_for(self, BASE_CURRENCY), currency)
            except ObjectNotFound:
                raise PriceNotFound()
