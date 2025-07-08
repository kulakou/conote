from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.notetaking.models.notes import NoteType


class NoteSchemaShortened(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class NoteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    text: Optional[str]
    link: Optional[str]
    type: str
    created_by: int
    room_id: int


class NoteCreateSchema(BaseModel):
    name: str
    text: Optional[str] = None
    link: Optional[str] = None
    type: NoteType
    created_by: int
    room_id: int
