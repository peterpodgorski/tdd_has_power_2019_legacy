from decimal import Decimal

import pytest

from constants import GBP, EUR, USD
from product import Price, Product, PriceNotFound
from utils import exchange


@pytest.fixture(scope="function")
def fake_db():
    Product.objects.clear()
    Price.objects.clear()


@pytest.mark.usefixtures('fake_db')
class TestPriceForCurrencyIs:
    @pytest.mark.parametrize('currency', [GBP, EUR, USD])
    def test_taken_from_product_if_set_on_it(self, currency):
        product = Product()
        product.save()

        price_gbp = Price(product, Decimal('100.00'), currency)
        price_gbp.save()

        assert product.get_price(currency) == price_gbp.amount

    @pytest.mark.parametrize('currency', [GBP, EUR, USD])
    def test_taken_from_parent_if_not_set_on_product(self, currency):
        parent = Product()
        parent.save()

        product = Product(parent_id=parent.id)
        product.save()

        price_gbp = Price(parent, Decimal('42.00'), currency)
        price_gbp.save()

        assert product.get_price(currency) == price_gbp.amount


@pytest.mark.usefixtures('fake_db')
class TestPriceForCurrencyIsExchangedFrom:
    @pytest.mark.parametrize('currency', [EUR, USD])
    def test_product_base_when_only_base_price_present_on_product(self, currency):
        product = Product()
        product.save()

        price_gbp = Price(product, Decimal('100.00'), GBP)
        price_gbp.save()

        assert product.get_price(currency) == exchange(price_gbp.amount, currency)

    @pytest.mark.parametrize('currency', [EUR, USD])
    def test_parent_base_when_only_base_price_set_on_parent(self, currency):
        parent = Product()
        parent.save()

        product = Product(parent_id=parent.id)
        product.save()

        price_gbp = Price(parent, Decimal('42.00'), GBP)
        price_gbp.save()

        assert product.get_price(currency) == exchange(price_gbp.amount, currency)


@pytest.mark.usefixtures('fake_db')
def test_get_price_raises_PriceNotFound_when_no_price_set_on_product_and_parent():
    product = Product()
    product.save()

    with pytest.raises(PriceNotFound):
        product.get_price(EUR)
