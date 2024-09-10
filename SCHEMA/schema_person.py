from pydantic import BaseModel, Field, model_validator
from typing import Optional

class PersonCreate(BaseModel):
    name: str
    password: str = Field(min_length=6, max_length=16)
    confirm_password: str

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password != confirm_password:
            raise ValueError('Passwords do not match!!')
        return values

class PersonDisplay(BaseModel):
    id: int
    name: str

    model_config = {
        'from_attributes': True
    }
    
class PersonUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6, max_length=16)
    confirm_password: str

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password != confirm_password:
            raise ValueError('Passwords do not match!!')
        return values

