from SERVICE.services_course import CourseServices
from DB.models import CourseModel, TeacherModel, ClassModel
from ENUMS.object_type_str import ObjectToSTR
from id_manager import UniqueID
from SCHEMA.schemas import CourseCreate, CourseDisplay, CourseUpdate
from USECASE.manage_object import ObjectUseCase
from ENUMS.object_type_digit import ObjectDigits
from UTILITY.custom_error import CustomError


from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

class CourseUseCase(ObjectUseCase[CourseServices]):
    def __init__(self, course_service: CourseServices, unique_id: UniqueID):
        super().__init__(course_service, unique_id, ObjectToSTR.COURSE)
    
    async def create(self, new_course: CourseCreate):
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
            
        teacher = await self.service.get_object_by_id_filter_model(new_course.teacher_id, TeacherModel)
        if not teacher:
            raise CustomError.existince_check(new_course.teacher_id, ObjectToSTR.TEACHER, False)
        
        classroom = await self.service.get_object_by_id_filter_model(new_course.class_id, ClassModel)
        if not classroom:
            raise CustomError.existince_check(new_course.class_id, ObjectToSTR.CLASSROOM, False)
        
        course_id = self.unique_id.insert(ObjectDigits.COURSE.value, ObjectToSTR.COURSE.value)
        db_course = await self.service.create_object(new_course, course_id)
        self.unique_id.save_to_dict(db_course.name, db_course.id, ObjectToSTR.COURSE.value)
        
        return db_course
        
    async def update(self, updated_course: CourseModel, course_id: int):
        temp = await self.service.get_object_by_id(course_id) 
        course = await self.service.update_obj(updated_course, temp)
        return CourseDisplay.model_validate(course)
