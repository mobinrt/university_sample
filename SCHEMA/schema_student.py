from pydantic import BaseModel, Field
from enum import Enum

from SCHEMA.schema_person import PersonCreate, PersonDisplay, PersonUpdate

class Major(str, Enum):
    computer_science = 'Computer Science'
    electrical_engineering = 'Electrical Engineering'
    mathematics = 'Mathematics'
    physics = 'Physics'

class StudentBase(BaseModel):
    id: int = Field(..., pattern=r'^\d{8}$')
    password: str

class StudentCreate(PersonCreate):
    major: Major = Field(..., description='Select your field: ' 
                            '1) computer_science '
                            '2) electrical_engineering '
                            '3) mathematics' 
                            '4) physics')

class StudentDisplay(PersonDisplay):
    major: Major

class StudentUpdate(PersonUpdate):
    pass
