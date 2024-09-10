from DB.models import StudentModel, CourseModel, TeacherModel, ClassModel
from id_manager import UniqueID
from ENUMS.object_type_str import ObjectToSTR
from ENUMS.object_type_digit import ObjectDigits
from SERVICE.services_object import ObjectServices
from UTILITY.custom_error import CustomError
from SCHEMA.schemas import CourseDisplay, CourseUpdate

from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class CourseServices(ObjectServices):
    def __init__(self, session: AsyncSession, unique_id: UniqueID):
        super().__init__(session, unique_id, CourseModel, ObjectToSTR.COURSE)
        
    async def create_object(self, new_course: CourseModel):
        if not new_course.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail='Name should not be blank!'
            )
            
        if new_course.end - new_course.start < timedelta(days=10):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The course must be at least 10 days long.'
            )
        
        teacher_query = select(TeacherModel).where(TeacherModel.id == new_course.teacher_id)
        classroom_query = select(ClassModel).where(ClassModel.id == new_course.class_id)
        
        async with self.session.begin():
            teacher_result = await self.session.execute(teacher_query)
            classroom_result = await self.session.execute(classroom_query)
            
            teacher = teacher_result.scalar_one_or_none()
            classroom = classroom_result.scalar_one_or_none()

        if not teacher:
            CustomError.existince_check(new_course.teacher_id, ObjectToSTR.TEACHER, 0)
        
        if not classroom:
            CustomError.existince_check(new_course.class_id, ObjectToSTR.CLASSROOM, 0)

        course_id = self.unique_id.insert(ObjectDigits.COURSE.value, ObjectToSTR.COURSE.value)
        
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
        self.unique_id.save_to_dict(db_course.name, db_course.id, ObjectToSTR.COURSE.value)
        return db_course

    async def update_obj(self, updated_course: CourseModel, course_id: int):
        temp = self.get_object_by_id(course_id) 
        course = await super().update_obj(updated_course, temp)
        return CourseDisplay.model_validate(course)
      
        
        