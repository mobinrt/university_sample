from SERVICE.services_student import StudentServices
from DB.models import StudentModel, CourseModel
from ENUMS.object_type_str import ObjectToSTR
from id_manager import UniqueID
from SCHEMA.schema_student import StudentCreate, StudentUpdate, StudentDisplay
from USECASE.manage_object import ObjectUseCase
from ENUMS.object_type_digit import ObjectDigits
from UTILITY.custom_error import CustomError

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

class StudentUseCase(ObjectUseCase[StudentServices]):
    def __init__(self, student_service: StudentServices, unique_id: UniqueID):
        super().__init__(student_service, unique_id, ObjectToSTR.STUDENT)
    
    async def create(self, new_student: StudentCreate):
        if not new_student.name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username should not be blank!')
        
        stu_id = self.unique_id.insert(ObjectDigits.STUDENT.value, ObjectToSTR.STUDENT.value)
                
        db_student = await self.service.create_object(new_student, stu_id)
        self.unique_id.save_to_dict(db_student.name, db_student.id, ObjectToSTR.STUDENT.value)
        return db_student
            

    async def update(self, student_update: StudentUpdate, login_student: StudentModel):
        current_stu = await self.service.update_obj(student_update, login_student)
        return StudentDisplay.model_validate(current_stu)
    
    async def attend_in_course(self, course_id: int, current_user: StudentModel):
        course = await self.service.get_object_by_id_filter_model(course_id, CourseModel)
        if not course:
            CustomError.existince_check(course_id, ObjectToSTR.COURSE, False)

        is_enrolled = await self.service.is_student_enrolled_in_course(course_id, current_user.id)
        if is_enrolled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You are already enrolled in course {course.name}."
            )

        await self.service.enroll_student_in_course(course_id, current_user.id)

        return {"message": f"You are enrolled in course {course.name}."}
         