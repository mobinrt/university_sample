from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class CourseCreate(BaseModel):
    name: str
    start: date
    end: date
    teacher_id: int
    class_id: int

class CourseDisplay(BaseModel):
    id: int
    name: str
    start: date
    end: date
    teacher_id: int
    class_id: int
    #student_ids: Optional[List[int]] = None

    model_config = {
        'from_attributes': True
    }
    
class CourseUpdate(BaseModel):
    name: str
    start: date
    end: date
    

class ClassCreate(BaseModel):
    id: int
    
class ClassDisplay(BaseModel):
    id: int
    
    model_config = {
        'from_attributes': True
    }
            
class TokenDisplay(BaseModel):
    access_token: str
    token_type: str
    
    model_config = {
        'from_attributes': True
    }
    
class UserDisplay(BaseModel):
    id: int
    name: str
    
    model_config = {
        'from_attributes': True
    }  
    