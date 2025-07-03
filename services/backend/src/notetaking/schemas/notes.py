from typing import Optional
from pydantic import BaseModel, ConfigDict


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
