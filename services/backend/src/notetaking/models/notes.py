from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class NoteType(Enum):
    LINK = "link"
    TEXT = "text"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    text: Mapped[str] = mapped_column(sa.String, nullable=True, default=None)
    link: Mapped[str] = mapped_column(sa.String, nullable=True, default=None)
    type: Mapped[NoteType] = mapped_column(sa.String, nullable=False)
    created_by: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    room_id: Mapped[int] = mapped_column(sa.ForeignKey("rooms.id"), nullable=False)
