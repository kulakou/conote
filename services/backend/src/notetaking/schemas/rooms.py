from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from src.notetaking.schemas.notes import NoteSchemaShortened


class RoomSchemaShortened(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RoomSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: Optional[int]
    type: str
    created_by: int
    notes: List[NoteSchemaShortened]


class RoomCreateSchema(BaseModel):
    name: str
    type: str
