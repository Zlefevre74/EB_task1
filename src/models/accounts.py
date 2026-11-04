from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import UUID, uuid4
from datetime import date
from .users import Base
from .orders import _values
from enums.billing import PaymentMethod
import sqlalchemy as sa



class AccountModel(Base):
    __tablename__ = 'accounts'
    __table_args__ = (
        sa.UniqueConstraint('account_number', name='uq_account_number'),
        sa.Index('ix_accounts_created', sa.desc('created_at'), sa.desc('id')),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(sa.String())
    account_number: Mapped[str] = mapped_column(sa.String(),
                                                nullable=False)
    opened_on: Mapped[date] = mapped_column(sa.Date())
    billing_profile: Mapped['BillingProfileModel | None'] = relationship(
        back_populates='account', uselist=False
    )

class BillingProfileModel(Base):
    __tablename__ = 'billing_profiles'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(
     sa.ForeignKey('accounts.id'), nullable=False, unique=True
    )
    payment_method: Mapped[PaymentMethod] = mapped_column(
        sa.Enum(PaymentMethod, name='payment_method',
        values_callable=_values)
    )
    currency: Mapped[str] = mapped_column(sa.String(3))
    account: Mapped['AccountModel'] = relationship(back_populates='billing_profile')
    billing_email: Mapped[str] = mapped_column(sa.String())