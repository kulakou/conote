from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from src.notetaking.schemas.notes import NoteSchemaShortened


class RoomSchemaShortened(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: Optional[int]
    created_by: int


class RoomSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: Optional[int]
    type: str
    created_by: int
    notes: List[NoteSchemaShortened]


class RoomCodeSchema(BaseModel):
    code: int


class RoomCreateSchema(BaseModel):
    name: str
    type: str


class RoomUpdateSchema(BaseModel):
    name: str
    type: str
    code: Optional[int]
