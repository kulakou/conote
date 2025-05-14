import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class TelegramUser(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    tg_username: Mapped[str] = mapped_column(index=True, unique=True)
    tg_id: Mapped[str] = mapped_column(sa.BigInteger, index=True, unique=True)
