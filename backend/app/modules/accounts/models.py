from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, Boolean, DateTime, Identity, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    start_balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        server_default='0'
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        server_default='RUB'
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default='false'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "currency IN ('RUB')",
            name="ck_accounts_currency"
        ),
        CheckConstraint(
            "length(btrim(name)) > 0",
            name="ck_accounts_name_not_empty"
        ),
        CheckConstraint(
            "start_balance <> 'NaN'::numeric",
            name="ck_accounts_start_balance_not_nan"
        )
    )