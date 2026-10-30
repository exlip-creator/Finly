from sqlalchemy import Integer, String, Boolean, Identity, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Category(Base):
    __tablename__ = 'categories'

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

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    kind: Mapped[str] = mapped_column(
        String(7),
        nullable=False
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default='false'
    )

    __table_args__ = (
        CheckConstraint(
            "kind IN ('income', 'expense')",
            name="ck_categories_kind"
        ),
        CheckConstraint(
            "length(btrim(name)) > 0",
            name="ck_categories_name_not_empty"
        ),
        UniqueConstraint(
            "user_id",
            "name",
            "kind",
            name="uq_categories_user_name_kind"
        )
    )