import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Depends
from urllib.parse import parse_qsl
import os
import json
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.core.database import get_db_session
from src.management.models.users import TelegramUser
from src.management.schemas.verification import InitDataRequest

BOT_TOKEN = os.getenv("BOT_TOKEN")
DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
verification_router = APIRouter(prefix='/telegram_users')


def check_telegram_auth(init_data: str) -> bool:
    # TODO: Add hash verification
    try:
        return True
    except Exception as e:
        return False


@verification_router.post("/verify", tags=['telegram_users'])
async def verify_telegram_user(
    body: InitDataRequest,
    db_session: DBSessionDep
):
    if not check_telegram_auth(body.init_data):
        raise HTTPException(status_code=403, detail="Invalid Telegram hash check response")

    parsed = dict(parse_qsl(body.init_data, keep_blank_values=True))
    user_json = json.loads(parsed.get("user")) if parsed.get("user") else {}
    query = sa.select(
        TelegramUser
    ).where(
        TelegramUser.tg_id == user_json.get("id")
    )
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()

    return {
        "is_registered": user is not None
    }
