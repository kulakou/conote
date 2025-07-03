import sqlalchemy as sa

from typing import Annotated
from fastapi import Depends, HTTPException, Path, Query
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.notetaking.models.rooms import Room, RoomType
from src.notetaking.models.notes import Note
from src.notetaking.schemas.rooms import RoomSchema, RoomSchemaShortened
from src.management.models.users import TelegramUser

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

rooms_router = APIRouter(
    prefix='/rooms'
)


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
