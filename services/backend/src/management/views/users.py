import random
from typing import Annotated

import sqlalchemy as sa
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.management.models.users import TelegramUser
from src.management.schemas.users import TelegramUserRegisterSchema
from src.notetaking.models.rooms import Room, RoomType

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


telegram_users_router = APIRouter(
    prefix='/telegram_users'
)


@telegram_users_router.post(
    path='/register',
    tags=['telegram_users']
)
async def register(
        data: TelegramUserRegisterSchema,
        db_session: DBSessionDep,
):

    # NOTE: Create user in database
    telegram_user = TelegramUser(**data.dict(exclude={"code"}))

    try:
        db_session.add(telegram_user)
        await db_session.commit()
        await db_session.refresh(telegram_user)
    except sa.exc.IntegrityError:
        return {"error": "Error during registration process"}

    # NOTE: Create private room for created user in database
    room = Room(
        name="My Notes", type=RoomType.SINGLE_SEAT.value,
        users=[telegram_user, ], created_by=telegram_user.id
    )

    # NOTE: If code is provided - add user to shared room
    target_room = None
    if data.code:
        query = sa.select(
            Room
        ).options(
            sa.orm.selectinload(Room.users)
        ).where(
            Room.code == data.code
        )
        result = await db_session.execute(query)
        target_room = result.scalar_one_or_none()
        if target_room:
            target_room.users.append(telegram_user)

    # NOTE: Save updated Room objects to database
    try:
        db_session.add(room)
        if target_room:
            db_session.add(target_room)
        await db_session.commit()
    except sa.exc.IntegrityError:
        return {"error": "Error during registration process"}

    return {"error": None, "data": data}


@telegram_users_router.get(
    path='/exists',
    tags=['telegram_users']
)
async def exists(tg_id: int, db_session: DBSessionDep):
    query = sa.select(sa.exists().where(TelegramUser.tg_id == tg_id))
    response = await db_session.execute(query)
    telegram_user_exists = response.scalar()
    return {"error": None, "data": {"tg_id": tg_id, "exists": telegram_user_exists}}
