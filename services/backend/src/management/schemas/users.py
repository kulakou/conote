from typing import Optional

from pydantic import BaseModel, ConfigDict


class TelegramUserSchema(BaseModel):
    id: int
    tg_username: str
    tg_id: int

    model_config = ConfigDict(from_attributes=True)


class TelegramUserRegisterSchema(BaseModel):
    tg_username: str
    tg_id: int
    code: Optional[int] = None
