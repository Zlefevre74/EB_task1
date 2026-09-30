import enum
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta


class SubscriptionType(enum.StrEnum):
    BASIC = 'basic'
    PRO = 'pro'


class BillingPeriod(enum.StrEnum):
    MONTHLY = 'monthly', 1, Decimal('0')
    ANNUAL = 'annual', 12, Decimal('20')

    months: int
    discount: Decimal

    def __new__(cls, value: str, months: int, discount: Decimal) -> 'BillingPeriod':
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.months = months
        obj.discount = discount
        return obj

    def expiry_from(self, moment: datetime) -> datetime:
        return moment + relativedelta(months=self.months)