import sqlalchemy as sa

from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.notetaking.models.notes import Note
from src.notetaking.schemas.notes import NoteSchema

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

notes_router = APIRouter(
    prefix='/notes'
)


@notes_router.get(
    path="/{note_id}",
    tags=["notes"],
    response_model=NoteSchema
)
async def get_single_room(
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
