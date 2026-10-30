from datetime import datetime
from sqlalchemy import DateTime, Identity, Integer, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "email = lower(btrim(email)) AND length(email) > 0",
            name='ck_users_email_normal'
        ),
    )