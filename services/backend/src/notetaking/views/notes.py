import sqlalchemy as sa

from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.notetaking.models.rooms import Room
from src.management.models.users import TelegramUser
from src.notetaking.models.notes import Note
from src.notetaking.schemas.notes import NoteSchema, NoteCreateSchema

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

notes_router = APIRouter(
    prefix='/notes'
)


@notes_router.get(
    path="/{note_id}",
    tags=["notes"],
    response_model=NoteSchema
)
async def get_single_note(
    db_session: DBSessionDep,
    note_id: int
):
    query = (
        sa.select(Note)
        .where(
            Note.id == note_id
        )
    )
    result = await db_session.execute(query)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=404, detail="Такой записки не существует")

    response_content = NoteSchema.model_validate(note).model_dump()

    return JSONResponse(status_code=200, content=response_content)

@notes_router.delete(
    path="/{note_id}",
    tags=["notes"]
)
async def delete_note(
    db_session: DBSessionDep,
    note_id: int,
    tg_id: int
):
    # Проверим, что записка существует и пользователь имеет доступ
    query = sa.select(Note).join(Room).join(Room.users).where(
        Note.id == note_id,
        TelegramUser.tg_id == tg_id
    )
    result = await db_session.execute(query)
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Записка не найдена или нет доступа")

    await db_session.delete(note)
    await db_session.commit()

    return JSONResponse(status_code=200, content={"status": "deleted"})


@notes_router.post(
    path="",
    tags=["notes"],
    response_model=NoteSchema
)
async def create_note(
    note_data: NoteCreateSchema,
    db_session: DBSessionDep,
):
    # Проверка доступа
    query = sa.select(Room).join(Room.users).where(
        Room.id == note_data.room_id,
        TelegramUser.tg_id == note_data.created_by
    )
    result = await db_session.execute(query)
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=403, detail="Нет доступа к комнате")

    note = Note(
        name=note_data.name,
        text=note_data.text,
        link=note_data.link,
        type=note_data.type.value,
        room_id=note_data.room_id,
        created_by=note_data.created_by
    )

    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)

    return NoteSchema.model_validate(note)
