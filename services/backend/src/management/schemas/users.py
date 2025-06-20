from typing import Optional

from pydantic import BaseModel


class TelegramUserSchema(BaseModel):
    id: int
    tg_username: str
    tg_id: int


class TelegramUserRegisterSchema(BaseModel):
    tg_username: str
    tg_id: int
    code: Optional[int] = None
