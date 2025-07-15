import random

import sqlalchemy as sa

from typing import Annotated
from fastapi import Depends, HTTPException, Path, Query
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.notetaking.models.rooms import Room, RoomType, telegram_users_rooms_association
from src.notetaking.models.notes import Note
from src.notetaking.schemas.rooms import RoomSchema, RoomCodeSchema, RoomUpdateSchema, RoomSchemaShortened, RoomCreateSchema
from src.management.models.users import TelegramUser

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

rooms_router = APIRouter(
    prefix='/rooms'
)

@rooms_router.get(
    path='/code/generated',
    tags=["rooms"]
)
async def generate_room_code(db_session: DBSessionDep):
    retries = 10
    for _ in range(0, retries):
        random_code = random.randrange(100000, 999999)
        query = sa.select(Room).where(Room.code == random_code)
        result = await db_session.execute(query)
        room = result.scalar_one_or_none()
        if not room:
            return random_code
    return None


@rooms_router.get(
    path='',
    tags=["rooms"]
)
async def get_user_rooms(
        tg_id: int,
        db_session: DBSessionDep,
        page: int = Query(1, ge=1),
        page_size: int = Query(5, ge=1, le=50),
):
    query = sa.select(
        Room
    ).join(
        Room.users
    ).where(
        TelegramUser.tg_id == tg_id,
        Room.type != 'single_seat_private'
    ).order_by(
        Room.id
    ).offset(
        (page - 1) * page_size
    ).limit(
        page_size
    )
    result = await db_session.execute(query)
    rooms = [
        RoomSchemaShortened.model_validate(room).model_dump()
        for room in result.scalars().all()
    ]

    count_query = sa.select(
        sa.func.count()
    ).select_from(
        Room
    ).where(
        TelegramUser.tg_id == tg_id,
        Room.type != 'single_seat_private'
    )
    total_rooms = (await db_session.execute(count_query)).scalar()
    return JSONResponse(status_code=200, content={"rooms": rooms, "total_rooms": total_rooms})


@rooms_router.get(
    path='/private',
    tags=["rooms"]
)
async def get_private_room(
    tg_id: int,
    db_session: DBSessionDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50),
):
    query = sa.select(
        Room
    ).join(
        Room.users
    ).where(
        TelegramUser.tg_id == tg_id,
        Room.type == 'single_seat_private'
    )
    result = await db_session.execute(query)
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(status_code=404, detail="Такой комнаты не существует")

    # Запрос на общее количество записок
    count_query = sa.select(sa.func.count()).select_from(Note).where(Note.room_id == room.id)
    total_notes = (await db_session.execute(count_query)).scalar()

    # Запрос на записки текущей страницы
    notes_query = (
        sa.select(Note)
        .where(Note.room_id == room.id)
        .order_by(Note.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    notes_result = await db_session.execute(notes_query)
    notes = notes_result.scalars().all()

    # Ручной сбор JSON (обход схемы, чтобы явно передать notes и total)
    return JSONResponse(status_code=200, content={
        "id": room.id,
        "name": room.name,
        "code": room.code,
        "type": room.type,
        "created_by": room.created_by,
        "notes": [{"id": note.id, "name": note.name} for note in notes],
        "total_notes": total_notes
    })


@rooms_router.get(
    path="/{room_id}",
    tags=["rooms"],
)
async def get_single_room(
    db_session: DBSessionDep,
    room_id: int,
    tg_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50),
):
    # Получаем комнату + пользователей (но без записок на этом этапе)
    query = (
        sa.select(Room)
        .join(Room.users)
        .where(
            Room.id == room_id,
            TelegramUser.tg_id == tg_id
        )
        .options(
            sa.orm.selectinload(Room.users)
        )
    )
    result = await db_session.execute(query)
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(status_code=404, detail="Такой комнаты не существует")

    # Запрос на общее количество записок
    count_query = sa.select(sa.func.count()).select_from(Note).where(Note.room_id == room_id)
    total_notes = (await db_session.execute(count_query)).scalar()

    # Запрос на записки текущей страницы
    notes_query = (
        sa.select(Note)
        .where(Note.room_id == room_id)
        .order_by(Note.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    notes_result = await db_session.execute(notes_query)
    notes = notes_result.scalars().all()

    # Ручной сбор JSON (обход схемы, чтобы явно передать notes и total)
    return JSONResponse(status_code=200, content={
        "id": room.id,
        "name": room.name,
        "code": room.code,
        "type": room.type,
        "created_by": room.created_by,
        "notes": [ {"id": note.id, "name": note.name} for note in notes ],
        "total_notes": total_notes
    })

@rooms_router.post(
    path='',
    tags=["rooms"]
)
async def create_room(
        db_session: DBSessionDep,
        data: RoomCreateSchema,
        tg_id: int
):
    import time
    time.sleep(2)
    query = sa.select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    try:
        result = await db_session.execute(query)
        telegram_user = result.scalar_one_or_none()
        if not telegram_user:
            raise Exception
    except Exception as e:
        raise HTTPException(status_code=500, detail="Telegram user can't be fetched")

    room_types = [
        RoomType.SHARED.value,
        RoomType.SINGLE_SEAT.value,
    ]
    if data.type not in room_types:
        raise HTTPException(
            status_code=422,
            detail=f"Type should be one from: {', '.join(room_types)}"
        )

    room = Room(name=data.name, type=data.type, created_by=tg_id)
    room.users.append(telegram_user)
    try:
        db_session.add(room)
        await db_session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error when creating room")
    return JSONResponse(status_code=200, content={"status": "OK"})


@rooms_router.delete(
    path="/{room_id}/leave",
    tags=["rooms"]
)
async def leave_room(
    db_session: DBSessionDep,
    room_id: int,
    tg_id: int
):
    # Получаем пользователя
    user_query = sa.select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    result = await db_session.execute(user_query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Удаляем связь между пользователем и комнатой
    delete_stmt = telegram_users_rooms_association.delete().where(
        telegram_users_rooms_association.c.room_id == room_id,
        telegram_users_rooms_association.c.telegram_user_id == user.id
    )

    await db_session.execute(delete_stmt)
    await db_session.commit()

    return JSONResponse(status_code=200, content={"status": "left"})


@rooms_router.post(
    path="/join",
    tags=["rooms"]
)
async def join_to_room(
    tg_id: int,
    data: RoomCodeSchema,
    db_session: DBSessionDep
):
    user_query = sa.select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    result = await db_session.execute(user_query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    room_query = sa.select(
        Room
    ).where(
        Room.code == data.code
    ).options(
        sa.orm.selectinload(Room.users)
    )
    result = await db_session.execute(room_query)
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="Комнаты с таким кодом не существует")
    if user in room.users:
        raise HTTPException(status_code=400, detail="Ты уже состоишь в этой комнате")

    room.users.append(user)
    db_session.add(room)
    await db_session.commit()
    return JSONResponse(status_code=200, content={"status": "updated"})


@rooms_router.put(
    path="/{room_id}",
    tags=["rooms"]
)
async def update_room(
    room_id: int,
    tg_id: int,
    data: RoomUpdateSchema,
    db_session: DBSessionDep
):
    query = sa.select(Room).where(Room.id == room_id)
    result = await db_session.execute(query)
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    if room.created_by != tg_id:
        raise HTTPException(status_code=403, detail="У тебя нет прав на редактирование")

    if data.type != RoomType.SHARED.value and data.code is not None:
        raise HTTPException(status_code=400, detail="Приватная комната не должна иметь код")

    room.name = data.name
    room.type = data.type
    room.code = data.code

    try:
        await db_session.commit()
        return JSONResponse(status_code=200, content={"status": "updated"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении комнаты")


@rooms_router.post(
    path="/{room_id}/code",
    tags=["rooms"]
)
async def update_room_code(
    room_id: int,
    tg_id: int,
    data: RoomCodeSchema,
    db_session: DBSessionDep
):
    query = sa.select(Room).where(Room.id == room_id)
    result = await db_session.execute(query)
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    if room.created_by != tg_id:
        raise HTTPException(status_code=403, detail="У тебя нет прав на редактирование")

    room.code = data.code
    room.type = RoomType.SHARED.value

    try:
        await db_session.commit()
        return JSONResponse(status_code=200, content={"status": "updated"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении комнаты")
