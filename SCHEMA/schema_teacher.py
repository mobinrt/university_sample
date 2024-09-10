from pydantic import BaseModel, Field
from enum import Enum

from SCHEMA.schema_person import PersonCreate, PersonDisplay, PersonUpdate

class TeacherBase(BaseModel):
    id: int = Field(..., pattern=r'^\d{6}$')
    password: str

class TeacherCreate(PersonCreate):
    pass

class TeacherDisplay(PersonDisplay):
    pass

class TeacherUpdate(PersonUpdate):
    pass
