from DB.models import CourseModel
from ENUMS.object_type_str import ObjectToSTR
from ENUMS.object_type_digit import ObjectDigits
from SERVICE.services_object import ObjectServices
from UTILITY.custom_error import CustomError
from SCHEMA.schemas import CourseDisplay, CourseUpdate

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class CourseServices(ObjectServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CourseModel)
        
    async def create_object(self, new_course: CourseModel, course_id):
        db_course = self.model(
            id=course_id,
            name=new_course.name,
            start=new_course.start,
            end=new_course.end,
            teacher_id=new_course.teacher_id,
            class_id=new_course.class_id,
        )
        
        self.session.add(db_course)
        await self.session.commit()
        await self.session.refresh(db_course)
        return db_course

      
        
        