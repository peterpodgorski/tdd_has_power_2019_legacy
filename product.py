from uuid import uuid4

from constants import BASE_CURRENCY
from fake_django import ObjectNotFound, Manager, Model
from utils import exchange


class Price(Model):
    objects = Manager()

    def __init__(self, product, amount, currency):
        self.id = uuid4()
        self.product = product
        self.product_id = product.id

        self.amount = amount
        self.currency = currency


class Product(Model):
    objects = Manager()

    def __init__(self, parent_id=None):
        self.id = uuid4()
        self.parent_id = parent_id

        self._parent_cache = None

    def get_price(self, currency):
        if self.parent_id is None:
            price = Price.objects.filter(product_id=self.id, currency=currency)
            if price:
                return price[0].amount
            else:
                to_exchange_price = Price.objects.get(
                    product_id=self.id, currency=BASE_CURRENCY
                )
                return exchange(to_exchange_price.amount, currency)
        else:
            try:
                price = Price.objects.get(product_id=self.id, currency=currency)
            except ObjectNotFound:
                try:
                    price = Price.objects.get(
                        product_id=self.parent_id, currency=currency
                    )
                except ObjectNotFound:
                    try:
                        to_exchange_price = Price.objects.get(
                            product_id=self.id, currency=BASE_CURRENCY
                        )
                        return exchange(to_exchange_price.amount, currency)
                    except ObjectNotFound:
                        to_exchange_price = Price.objects.get(
                            product_id=self.parent_id, currency=BASE_CURRENCY
                        )
                        return exchange(to_exchange_price.amount, currency)
                else:
                    return price.amount
            else:
                return price.amount
