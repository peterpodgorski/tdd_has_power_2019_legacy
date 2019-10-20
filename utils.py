from decimal import Decimal

from constants import USD, EUR


def exchange(amount, to_currency):
    rates = {EUR: Decimal('1.16'), USD: Decimal('1.29')}
    return amount * rates[to_currency]