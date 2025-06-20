from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.notetaking.models.rooms import telegram_users_rooms_association


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    tg_username: Mapped[str] = mapped_column(index=True, unique=True)
    tg_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, unique=True)
    rooms: Mapped[List["Room"]] = sa.orm.relationship(
        secondary=telegram_users_rooms_association,
        back_populates="users",
    )
