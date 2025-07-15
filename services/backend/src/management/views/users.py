from typing import Annotated

import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.management.models.users import TelegramUser
from src.management.schemas.users import TelegramUserRegisterSchema
from src.notetaking.models.rooms import Room, RoomType
from src.notetaking.models.notes import Note

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
    target_room = None
    if data.code:
        query = sa.select(Room).options(
            sa.orm.selectinload(Room.users)
        ).where(Room.code == data.code)
        result = await db_session.execute(query)
        target_room = result.scalar_one_or_none()
        if not target_room:
            raise HTTPException(status_code=404, detail="Комнаты с таким кодом не существует")

    # NOTE: Create user in database
    telegram_user = TelegramUser(**data.dict(exclude={"code"}))

    try:
        db_session.add(telegram_user)
        await db_session.commit()
        await db_session.refresh(telegram_user)
        if target_room:
            await db_session.refresh(target_room)
    except sa.exc.IntegrityError:
        return {"error": "Error during registration process"}

    # NOTE: Create private room for created user in database
    room = Room(
        name="Приватная", type=RoomType.SINGLE_SEAT_PRIVATE.value,
        users=[telegram_user, ], created_by=telegram_user.tg_id
    )

    if data.code and target_room:
        target_room.users.append(telegram_user)

    # NOTE: Save updated Room objects to database
    try:
        db_session.add(room)
        if target_room:
            db_session.add(target_room)
        await db_session.commit()
        await db_session.refresh(room)
    except sa.exc.IntegrityError:
        return {"error": "Error during registration process"}

    note_text = Note(
        name="Пример текстовой записки", type="text",
        text="Здесь будет текстовое наполнение твоей записки",
        created_by=room.created_by, room_id=room.id
    )
    note_link = Note(
        name="Пример записки-ссылки", type="link",
        link="https://google.com", text="Эта ссылка ведет тебя в Google!",
        created_by=room.created_by, room_id=room.id
    )
    try:
        db_session.add(note_text)
        db_session.add(note_link)
        await db_session.commit()
    except sa.exc.IntegrityError:
        return {"error": "Error during registration process"}

    return {"error": None, "data": data}
