from enum import Enum
from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


telegram_users_rooms_association = sa.Table(
    "telegram_users_rooms_association",
    Base.metadata,
    sa.Column("telegram_user_id", sa.ForeignKey("telegram_users.id"), primary_key=True),
    sa.Column("room_id", sa.ForeignKey("rooms.id"), primary_key=True),
)


class RoomType(Enum):
    SINGLE_SEAT_PRIVATE = "single_seat_private"
    SINGLE_SEAT = "single_seat"
    SHARED = "shared"


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    code: Mapped[int] = mapped_column(sa.Integer, unique=True, nullable=True)
    type: Mapped[RoomType] = mapped_column(sa.String, nullable=False)
    created_by: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    users: Mapped[List["TelegramUser"]] = sa.orm.relationship(
        secondary=telegram_users_rooms_association,
        back_populates="rooms",
    )
