from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import Integer, String, Text, Numeric, Identity, ForeignKey, CheckConstraint, Date, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )

    account_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('accounts.id'),
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('categories.id'),
        nullable=False
    )

    kind: Mapped[str] = mapped_column(
        String(7),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18,2),
        nullable=False
    )

    occurred_at: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "amount > 0 AND amount <> 'NaN'::numeric",
            name="ck_transactions_amount"
        ),
        CheckConstraint(
            "kind IN ('income', 'expense')",
            name="ck_transactions_kind"
        ),
        Index(
            "idx_transactions_user_occured_at_id",
            "user_id",
            "occurred_at",
            "id"
        )
    )